import math
import numpy as np
from numpy import ndarray
from simulation import Simulate


def random_walk(col_pre, row_pre, dist='int'):
    if dist == 'nom':
        col_pre += np.random.normal(scale=30)
        row_pre += np.random.normal(scale=30)
        col_next: ndarray = np.clip(col_pre, 0, 90)
        row_next: ndarray = np.clip(row_pre, 0, 90)
        return col_next, row_next

    if dist == 'uni':
        x_next = np.random.uniform(0, 100)
        y_next = np.random.uniform(0, 100)

        return x_next, y_next

    if dist == 'int':
        col_pre += np.random.randint(10, 90)
        row_pre += np.random.normal(10, 90)
        col_next: ndarray = np.clip(col_pre, 0, 90)
        row_next: ndarray = np.clip(row_pre, 0, 90)
        return col_next, row_next


def make_triangle_pos(col_pre_pos, row_pre_pos, pre_intensity=100, triangle_radius=5):
    """
    閾値を上回った座標を中心とした3点の座標

    :param col_pre_pos: 前の集光点のy座標
    :param row_pre_pos: 前の集光点のx座標
    :param pre_intensity: 前の集光点の強度
    :param triangle_radius: 3点計測 (三角形) の外接円の半径

    :return:　x_list, y_list
    """
    col_list = []
    row_list = []
    # 閾値を上回った座標を中心に3点
    for i in range(0, 3):
        col = col_pre_pos + triangle_radius * np.cos(2 * i * np.pi / 3)
        row = row_pre_pos + triangle_radius * np.sin(2 * i * np.pi / 3)
        col_list.append(col)
        row_list.append(row)
    return col_list, row_list


sim = Simulate(num_beads=3, grid_step=0.1, spot_diameter=1)

# 蛍光ビーズの空間を作成
beads_matrix, beads_col, beads_row = sim.make_not_gaussian_beads(do_print=True)

# 蛍光ビーズの空間を描画する
sim.draw_not_gaussian_beads(not_gaussian_beads=beads_matrix)

# ランダムウォークおよび閾値判定の処理開始
# col_first, row_first = 50, 50  # ランダムウォークの初期位置
col_first = beads_col[0]
row_first = beads_row[0]
col_next = col_first
row_next = row_first
random_walk_threshold = 0.1  # ランダムウォーク時に用いる閾値
over_keikou_threshold = 0.1
count = 0  # とりあえずループのカウンタ
max_count = 3
signal = 0

trajectory_col = []
trajectory_row = []
trajectory_col.append(col_first)
trajectory_row.append(row_first)
i = 0
# 閾値を超えるまでランダムウォーク
print("ランダムウォーク開始")
print("ランダムウォーク開始座標: {0}, {1}".format(int(col_next), int(row_next)))
while signal <= random_walk_threshold:
    # はじめのランダムウォークはx_first, yを与えて輝度値を取得
    i += 1
    signal = sim.get_signal_simple(beads_matrix, int(col_next), int(row_next))
    print("{0}回目のsignal: {1}".format(i, signal))
    if signal >= random_walk_threshold:
        break
    col_next, row_next = random_walk(col_pre=col_next, row_pre=row_next)
    print("ランダムウォーク座標更新 (行, 列)", int(col_next), int(row_next))
    trajectory_col.append(col_next)
    trajectory_row.append(row_next)

# 閾値を上回ったときの座標は(x_next, y_next)
# この点を中心にしたいので変数名をx_pre, y_preにそれぞれ変更
print("閾値超えたときの座標 (行，列) = ({0}, {1})".format(col_next, row_next))
col_pre = col_next
row_pre = row_next
col_list, row_list = make_triangle_pos(col_pre_pos=col_pre, row_pre_pos=row_pre)  # 3点の集光点座標を返す

for i in range(len(col_list)):
    trajectory_col.append(col_list[i])
    trajectory_row.append(row_list[i])
# 座標をもとに3点順に集光，輝度値計測
# 輝度値のリスト signal_list を返してもらう?
print("3点計測開始")
while count < max_count:
    count += 1
    signal_list = []
    # ここで閾値検出後最初の計測 get_signal(x_list, y_list)
    for i in range(len(col_list)):
        signal = sim.get_signal_simple(beads_matrix, int(col_list[i]), int(row_list[i]))
        print("signal", signal)
        signal_list.append(signal)
    # signalを返してもらう signal_list = [sig0, sig1, sig2]
    # ここで蛍光検出数について条件分岐を挟む
    over_list = [i for i, x in enumerate(signal_list) if x >= over_keikou_threshold]
    len_over_list = len(over_list)
    print("len_oer_list: ",len_over_list)
    if len_over_list == 0:
        # 蛍光検出数が0
        # この時は3点計測の中心≒蛍光ビーズの中心
        # 中心座標は変えずに再度3点計測
        # 3点集光の座標リストだけを返す
        col_list, row_list = make_triangle_pos(col_pre_pos=col_pre, row_pre_pos=row_pre)
        for i in range(len(col_list)):
            trajectory_col.append(col_list[i])
            trajectory_row.append(row_list[i])

    elif len_over_list == 1:
        # 3点計測のうち1点だけ高い輝度値が得られた
        # 3点計測の中心を高い輝度値を検出した方向に移動して3点計測
        # とりあえず前の中心と高輝度値の座標の中点に集光
        over_keikou_threshold_x = col_list[over_list[0]]  # 蛍光の閾値 (keikou_threshold) を上回った時のx座標
        over_keikou_threshold_y = row_list[over_list[0]]  # 蛍光の閾値を上回った時のy座標

        # x_preの値を更新
        # x_preはもともと3点計測の中心点だった
        col_pre = math.ceil((col_pre + over_keikou_threshold_x) / 2)
        row_pre = math.ceil((row_pre + over_keikou_threshold_y) / 2)

        # 3点計測の座標リストを返す
        col_list, row_list = make_triangle_pos(col_pre_pos=col_pre, row_pre_pos=row_pre)
        for i in range(len(col_list)):
            trajectory_col.append(col_list[i])
            trajectory_row.append(row_list[i])

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
        col_list, row_list = make_triangle_pos(col_pre_pos=col_pre, row_pre_pos=row_pre)

        for i in range(len(col_list)):
            trajectory_col.append(col_list[i])
            trajectory_row.append(row_list[i])

    else:
        print("閾値を超えたのが3点 -> triangle_radiusが多分小さすぎる")
        print("いったん終了する")
        break

print("len(trajectory_row)",len(trajectory_row))