import math
from sys import exit
import numpy as np
import matplotlib.pyplot as plt
import cv2
from make_spot_pos import random_walk, make_triangle_pos, make_triangle_pos_inverse
from simulation import Simulate
from to_csv import log_random_walk, log_triangle

sim = Simulate(num_beads=10, grid_step=0.1, spot_diameter=1, do_print=True)
# animationを表示しないときはこの行
# sim.draw_not_gaussian_beads(sim.beads_matrix)
initial_beads = sim.beads_matrix
# sim.draw_not_gaussian_beads(initial_beads)
# print("type of initial_beads", initial_beads.dtype)

# cv2.imwrite('initial_beads_2.tiff', initial_beads)
# animationを表示するときはこの行
# fig, ax = plt.subplots()
# im = ax.imshow(sim.beads_matrix, cmap='gray', interpolation='nearest',
#                extent=(0, sim.col_grid_size, 0, sim.row_grid_size))
# ax.set_xlabel("row [µm]")
# ax.set_ylabel("col [µm]")

# for i in range(sim.num_frames):
#     shifted_beads_matrix = sim.move_beads_matrix(shift_amount=1)
#     im.set_data(shifted_beads_matrix)
#     plt.pause(0.1)  # pause to allow animation to be seen
#     sim.beads_matrix = shifted_beads_matrix

plt.show()


def shift_beads_matrix(beads_matrix, shift_amount):
    shifted_beads_matrix = np.roll(beads_matrix, shift=shift_amount, axis=1)
    return shifted_beads_matrix


# 信号が閾値よりも小さい限りランダムウォークを続ける
# 閾値を上回った時に同じ細胞を追跡していないかチェックする機構が必要
# あるいは次の呼び出し時に，閾値を超えた座標よりかなり離れた地点を指定する?
def do_random_walk(col0, row0, beads_matrix, try_count, total_num=0, max_count_random_walk=100):
    """
    実際にランダムウォークを実施する関数
    閾値を上回った時点で終了する
    :param beads_matrix:
    :param col0:
    :param row0:
    :param try_count: csvファイルに記録すために何回目のランダムウォークかを代入する
    :return:
    """
    # 閾値を超えるまでランダムウォーク
    # print("ランダムウォーク開始座標: ({0}, {1})".format(int(col0), int(row0)))
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
    # シグナルを格納するリスト
    random_signal = []

    # 無限ループ防止のためにmax_count_random_walkによるiteration回数の制限付き
    # countが3の倍数になるたびに、ビーズの位置を動かす
    for i in range(max_count_random_walk):
        # while count < max_count_random_walk:
        count += 1
        total_num += 1
        if total_num % 3 == 0:
            beads_matrix = shift_beads_matrix(beads_matrix, 10)
        # 信号取得
        _signal = sim.get_signal_simple(beads_matrix, int(_col_next), int(_row_next), count)
        random_signal.append(_signal)

        # 閾値を上回ったらcsvファイルに軌跡を書き込み，座標を返して終了
        if _signal >= random_walk_signal_threshold:
            log_random_walk(random_col_list=random_col, random_row_list=random_row,
                            random_signal_list=random_signal, total_num=total_num, filename=try_count)
            # print("count", count)
            return _col_next, _row_next, beads_matrix, total_num

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
def do_triangle(col0, row0, beads_matrix, try_count, total_num):
    """
    3点計測を行うための関数
    3点計測で閾値を上回った数が0になった時点でその座標を返して終了
    :param beads_matrix:
    :param col0:
    :param row0:
    :param try_count:
    :return: len(over_list
    """
    # print(" 3点計測最初の中心: (行，列) = ({0}, {1})".format(int(col0), int(row0)))
    col_pre, row_pre = col0, row0
    trajectory_col_center, trajectory_row_center = [], []
    trajectory_col_center.append(col_pre)
    trajectory_row_center.append(row_pre)
    keikou_threshold = 0.1
    # 3点計測のリスト作成
    col_list, row_list = make_triangle_pos(col_pre_pos=col_pre, row_pre_pos=row_pre)

    # 座標をもとに3点順に集光，輝度値計測
    # 輝度値のリスト signal_list を返してもらう?
    # print("3点計測開始")
    count = 0
    max_count = 100
    len_over_list_list = []  # over_listの要素数を格納するリスト
    zero_count = 0
    # とりあえずcountの上限を設定して無限ループを避ける
    while count < max_count:
        count += 1
        total_num += 1
        if total_num % 3 == 0:
            beads_matrix = shift_beads_matrix(beads_matrix, 10)
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
            zero_count += 1
            # 蛍光検出数が0
            # この時は座標を特定できたとしてcsvに書き込んで終了する
            # 戻り値はこの時の座標
            # この時は中心そのままで逆条件で照射
            if zero_count == 1:
                trajectory_row_center.append(row_pre)
                trajectory_col_center.append(col_pre)
                col_list, row_list = make_triangle_pos_inverse(col_pre_pos=col_pre, row_pre_pos=row_pre)

            elif zero_count == 2:
                log_triangle(col_center_list=trajectory_col_center, row_center_list=trajectory_row_center,
                             len_over_list_list=len_over_list_list, total_num=total_num, filename=try_count)
                print("count", count)
                return trajectory_col_center[-1], trajectory_row_center[-1], beads_matrix, total_num

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
            zero_count = 0

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
            zero_count = 0

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
tracking_max_num = 3
start_value = 20
end_value = 80
col_pos_list = np.linspace(start_value, end_value, tracking_max_num).tolist()
row_pos_list = np.linspace(start_value, end_value, tracking_max_num).tolist()
after_triangle_col, after_triangle_row = [], []
over_threshold_num = 0
col_list, row_list = [], []
beads_matrix = sim.beads_matrix
print(int(col_pos_list[over_threshold_num]))
# とりあえずランダムウォークして閾値越えを3点見つける

while over_threshold_num < 3:
    if over_threshold_num == 0:
        col1, row1, beads_matrix, total_num = do_random_walk(col0=int(col_pos_list[over_threshold_num]),
                                                             row0=int(row_pos_list[over_threshold_num]),
                                                             beads_matrix=beads_matrix,
                                                             try_count=over_threshold_num + 1)
        col_list.append(col1)
        row_list.append(row1)
        over_threshold_num += 1
    else:
        col1, row1, beads_matrix, total_num = do_random_walk(col0=int(col_pos_list[over_threshold_num]),
                                                             row0=int(row_pos_list[over_threshold_num]),
                                                             beads_matrix=beads_matrix, total_num=total_num,
                                                             try_count=over_threshold_num + 1)
        col_list.append(col1)
        row_list.append(row1)
        over_threshold_num += 1

print("Done random_walk!!: ", total_num)
random_num = total_num
# 3点計測をそれぞれの閾値に対して順に実施
# 蛍光検出が終わった時点で0になった時のユーグリッド距離を調べる
for j in range(len(col_list)):
    col, row, beads_matrix, total_num = do_triangle(col_list[j], row_list[j], beads_matrix=beads_matrix,
                                                    total_num=total_num, try_count=j + 1)
    after_triangle_col.append(col)
    after_triangle_row.append(row)

print("random_num:{0}, triangle_num:{1}, total_num: {2}".format(random_num, total_num-random_num, total_num))

# print("len(after_triangle_row", len(after_triangle_row))
sim.draw_not_gaussian_beads(initial_beads)
# # ビーズを3時刻分移動
# for i in range(3):
#     beads_matrix = shift_beads_matrix(beads_matrix, 10)
#
#
# # 位置推定完了後に追跡開始
# # 追跡時の初期座標はafter_triangle_col, after_triangle_rowに格納してある
# print("Start tracking!!\n")
# tracking_col, tracking_row = [], []
# for j in range(len(col_list)):
#     col, row, beads_matrix, total_num = do_triangle(after_triangle_col[j], after_triangle_row[j], beads_matrix=beads_matrix, total_num=total_num, try_count=j+4)
#     after_triangle_col.append(col)
#     after_triangle_row.append(row)

# sim.draw_not_gaussian_beads(beads_matrix)
