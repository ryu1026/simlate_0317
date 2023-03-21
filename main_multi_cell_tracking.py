import math
from sys import exit
import numpy as np

from make_spot_pos import random_walk, make_triangle_pos
from simulation import Simulate
from to_csv import log_random_walk, log_triangle

sim = Simulate(num_beads=10, grid_step=0.1, spot_diameter=1)
# 蛍光ビーズの空間を作成
beads_matrix, beads_col, beads_row = sim.make_not_gaussian_beads_not_overlap()

draw_beads = True
# 蛍光ビーズの空間を描画する
for bead_col, bead_row in zip(beads_col, beads_row):
    print("beads_pos: (行, 列) = ({0}, {1}) = (y, x)".format(bead_col, bead_row))
if draw_beads:
    sim.draw_not_gaussian_beads(not_gaussian_beads=beads_matrix)


# 信号が閾値よりも小さい限りランダムウォークを続ける
# 閾値を上回った時に同じ細胞を追跡していないかチェックする機構が必要
# あるいは次の呼び出し時に，閾値を超えた座標よりかなり離れた地点を指定する?
def do_random_walk(col0, row0, try_count):
    """
    実際にランダムウォークを実施する関数
    閾値を上回った時点で終了する
    :param col0:
    :param row0:
    :param try_count: csvファイルに記録すために何回目のランダムウォークかを代入する
    :return:
    """
    # 閾値を超えるまでランダムウォーク
    print("ランダムウォーク開始座標: ({0}, {1})".format(int(col0), int(row0)))
    # 単純なループカウンタ
    count = 0
    # ランダムウォークの初期値
    _col_next, _row_next = col0, row0
    # ランダムウォークの軌跡のリスト
    random_col, random_row = [], []
    # 初期の座標を軌跡に追加
    random_col.append(col0)
    random_row.append(row0)
    # ランダムウォークのシグナルの閾値
    random_walk_signal_threshold = 0.1
    # ランダムウォークの最高iteration (無限ループにならないように)
    max_count_random_walk = 100
    # シグナルを格納するリスト
    random_signal = []

    # 無限ループ防止のためにmax_count_random_walkによるiteration回数の制限付き
    for i in range(max_count_random_walk):
        # while count < max_count_random_walk:
        count += 1
        # 信号取得
        _signal = sim.get_signal_simple(beads_matrix, int(_col_next), int(_row_next), count)
        random_signal.append(_signal)

        # 閾値を上回ったらcsvファイルに軌跡を書き込み，座標を返して終了
        if _signal >= random_walk_signal_threshold:
            log_random_walk(random_col_list=random_col, random_row_list=random_row,
                            random_signal_list=random_signal, filename=try_count)
            return _col_next, _row_next

        # 信号が閾値以下なら次の座標を設定
        _col_next, _row_next = random_walk(col_pre=_col_next, row_pre=_row_next)
        # ランダムウォークの履歴を記録
        random_col.append(_col_next)
        random_row.append(_row_next)
        # print("ランダムウォーク座標更新 (行, 列)", int(_col_next), int(_row_next))

    else:
        print("ランダムウォークの最大回数に到達しました")
        print("いったん終了します")
        exit()

# 閾値検出後はすぐに3点計測
# 内部でdo_random_walkも継続しないといけない?
def do_triangle(col0, row0, try_count):
    """
    3点計測を行うための関数
    3点計測で閾値を上回った数が0になった時点でその座標を返して終了
    :param col0:
    :param row0:
    :param try_count:
    :return: len(over_list
    """
    print(" 3点計測最初の中心: (行，列) = ({0}, {1})".format(int(col0), int(row0)))
    col_pre, row_pre = col0, row0
    trajectory_col_center, trajectory_row_center = [], []
    trajectory_col_center.append(col_pre)
    trajectory_row_center.append(row_pre)
    keikou_threshold = 0.1
    # 3点計測のリスト作成
    col_list, row_list = make_triangle_pos(col_pre_pos=col_pre, row_pre_pos=row_pre)

    # 座標をもとに3点順に集光，輝度値計測
    # 輝度値のリスト signal_list を返してもらう?
    print("3点計測開始")
    count = 0
    max_count = 100
    len_over_list_list = []  # over_listの要素数を格納するリスト

    # とりあえずcountの上限を設定して無限ループを避ける
    while count < max_count:
        count += 1
        signal_list = []
        for i in range(len(col_list)):
            # 3点を１つずつ渡して計測している
            signal = sim.get_signal_simple(beads_matrix, int(col_list[i]), int(row_list[i]), count)
            signal_list.append(signal)

        # ここで蛍光検出数について条件分岐
        over_list = [i for i, x in enumerate(signal_list) if x >= keikou_threshold]
        len_over_list = len(over_list)
        len_over_list_list.append(len_over_list)
        # print("len_over_list: ", len_over_list)
        # print("\n")

        if len_over_list == 0:
            # 蛍光検出数が0
            # この時は座標を特定できたとしてcsvに書き込んで終了する
            # 戻り値はこの時の座標
            trajectory_row_center.append(row_pre)
            trajectory_col_center.append(col_pre)
            log_triangle(col_center_list=trajectory_col_center[:-1], row_center_list=trajectory_row_center[:-1],
                         len_over_list_list=len_over_list_list, filename=try_count)
            return trajectory_col_center[-1], trajectory_row_center[-1]

        elif len_over_list == 1:
            # 3点計測のうち1点だけ高い輝度値が得られた
            # 3点計測の中心を高い輝度値を検出した方向に移動して3点計測
            # とりあえず前の中心と高輝度値の座標の中点に集光
            over_keikou_threshold_x = col_list[over_list[0]]  # 蛍光の閾値 (keikou_threshold) を上回った時のx座標
            over_keikou_threshold_y = row_list[over_list[0]]  # 蛍光の閾値を上回った時のy座標

            # x_preの値を更新
            # x_preはもともと3点計測の中心点だった
            # 更新した中心座標をtrajectory_col_centerに格納
            col_pre = math.ceil((col_pre + over_keikou_threshold_x) / 2)
            row_pre = math.ceil((row_pre + over_keikou_threshold_y) / 2)
            trajectory_col_center.append(col_pre)
            trajectory_row_center.append(row_pre)

            # 3点計測の座標リストを返す
            col_list, row_list = make_triangle_pos(col_pre_pos=col_pre, row_pre_pos=row_pre)

        elif len_over_list == 2:
            # 3点計測のうち2点で高い輝度値が得られた
            # 2点の中間値を次の中心にする
            over_keikou_threshold_x1, over_keikou_threshold_x2 = col_list[over_list[0]], col_list[over_list[1]]
            over_keikou_threshold_y1, over_keikou_threshold_y2 = row_list[over_list[0]], row_list[over_list[1]]

            # x_preの値を更新
            # x_preはもともと3点計測の中心点だった
            # keikou_thresholdを上回った二点の中間座標にx_pre, y_preを更新する
            # ここはmath.ceil((x_pre + over_keikou_threshold_x1 + over_keikou_threshold_x2) / 3)でもいいかも
            col_pre = math.ceil((over_keikou_threshold_x1 + over_keikou_threshold_x2) / 2)
            row_pre = math.ceil((over_keikou_threshold_y1 + over_keikou_threshold_y2) / 2)

            trajectory_col_center.append(col_pre)
            trajectory_row_center.append(row_pre)

            col_list, row_list = make_triangle_pos(col_pre_pos=col_pre, row_pre_pos=row_pre)

        else:
            print("閾値を超えたのが3点 -> triangle_radiusが多分小さすぎる")
            print("いったん終了する")
            break
    # whileループが終わった後の処理
    # この部分は一度だけ実行される
    else:
        print("3点計測を終了します")


# tracking_max_numは追跡する細胞数
# do_random_walkからは閾値を検出した時の座標が返ってくる
# do_triangleは閾値を検出したときの座標を初期位置としてlen_over_list=0の時の中心座標を返す
# ランダムウォークの初期位置


# Define the number of elements and the range of values
tracking_max_num = 4
start_value = 20
end_value = 80
col_pos_list = np.linspace(start_value, end_value, tracking_max_num).tolist()
row_pos_list = np.linspace(start_value, end_value, tracking_max_num).tolist()


for j in range(len(col_pos_list)):
    col1, row1 = do_random_walk(col0=int(col_pos_list[j]), row0=int(row_pos_list[j]), try_count=j + 1)
    col2, row2 = do_triangle(col0=col1, row0=row1, try_count=j + 1)
