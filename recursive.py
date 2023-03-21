import sys
import math
from to_csv import log_random_walk, log_csv
from simulation import Simulate
from make_spot_pos import random_walk, make_triangle_pos, log_signal_spot

sim = Simulate(num_beads=10, grid_step=0.1, spot_diameter=1)

# 蛍光ビーズの空間を作成
beads_matrix, beads_col, beads_row = sim.make_not_gaussian_beads_not_overlap()

# ランダムウォークおよび閾値判定の処理開始
random_col, random_row = [], []
random_signal = []
# ランダムウォークの初期位置
col_first, row_first = 50, 50
# ランダムウォークのtrajectoryを取る
random_col.append(col_first)
random_row.append(row_first)

# col_first, row_first = beads_col[0], beads_row[0]
col_next = col_first
row_next = row_first

# ランダムウォーク時に用いる閾値
random_walk_threshold = 0.1
over_keikou_threshold = 0.1

count = 0  # とりあえずループのカウンタ
max_count = 100
signal = 0  # signalの初期値

# 閾値を超えるまでランダムウォーク
print("ランダムウォーク開始座標: ({0}, {1})".format(int(col_next), int(row_next)))

# 信号が閾値よりも小さい限りランダムウォークを続ける
max_random_walk = 100
while signal <= random_walk_threshold and count < max_random_walk:
    count += 1

    # 信号取得 (col_next, row_next)を中心にスポットを作成してスポットの内部の信号の平均値を取得
    signal = sim.get_signal_simple(beads_matrix, int(col_next), int(row_next), count)
    random_signal.append(signal)
    if signal >= random_walk_threshold:
        break
    # 信号が閾値以下なら次の座標を設定
    col_next, row_next = random_walk(col_pre=col_next, row_pre=row_next)

    # ランダムウォークの履歴を記録
    random_col.append(col_next)
    random_row.append(row_next)
    print("ランダムウォーク座標更新 (行, 列)", int(col_next), int(row_next))

if count >= max_random_walk:
    print("ランダムウォークの最大回数に到達しました")
    print("プログラムを終了します")
    sys.exit()

# 閾値を上回ったときの座標は(x_next, y_next)
# この点を中心にしたいので変数名をx_pre, y_preにそれぞれ変更
print("over threshold at (行，列) = ({0}, {1}) = 最初の三点計測の中心".format(col_next, row_next))
col_pre = col_next
row_pre = row_next

# 3点計測の中心座標を記録するリスト
trajectory_col_center = []
trajectory_row_center = []
# 3点計測の最初の中心 (閾値を超えたときの座標)を代入
trajectory_col_center.append(col_pre)
trajectory_row_center.append(row_pre)

col_list, row_list = make_triangle_pos(col_pre_pos=col_pre, row_pre_pos=row_pre)  # 3点の集光点座標を返す

# 座標をもとに3点順に集光，輝度値計測
# 輝度値のリスト signal_list を返してもらう?
print("3点計測開始")
print("\n")
len_over_list_list = []
while count < max_count:
    count += 1
    signal_list = []

    for i in range(len(col_list)):
        # 3点を１つずつ渡して計測している
        signal = sim.get_signal_simple(beads_matrix, int(col_list[i]), int(row_list[i]), count)
        signal_list.append(signal)

    # ここで蛍光検出数について条件分岐
    over_list = [i for i, x in enumerate(signal_list) if x >= over_keikou_threshold]
    len_over_list = len(over_list)
    len_over_list_list.append(len_over_list)
    # print("len_over_list: ", len_over_list)
    # print("\n")

    if len_over_list == 0:
        # 蛍光検出数が0
        # この時は3点計測の中心≒蛍光ビーズの中心
        # 中心座標は変えずに再度3点計測
        # 3点集光の座標リストだけを返す
        # 最初に中心座標を格納
        trajectory_row_center.append(row_pre)
        trajectory_col_center.append(col_pre)

        # 次の集光点を決定 = 前と同じ
        col_list, row_list = make_triangle_pos(col_pre_pos=col_pre, row_pre_pos=row_pre)

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

print(len(len_over_list_list))
print(len(trajectory_col_center))
print("max_iterationに到達しました")
print("ランダムウォークの回数: {0}".format(len(random_row)))
log_random_walk(random_col_list=random_col, random_row_list=random_row, random_signal_list=random_signal)
log_csv(col_center_list=trajectory_col_center[:-1], row_center_list=trajectory_row_center[:-1],
        len_over_list_list=len_over_list_list)
draw_beads = True
# 蛍光ビーズの空間を描画する
for bead_col, bead_row in zip(beads_col, beads_row):
    print("beads_pos: (行, 列) = ({0}, {1}) = (y, x)".format(bead_col, bead_row))
if draw_beads:
    sim.draw_not_gaussian_beads(not_gaussian_beads=beads_matrix)
