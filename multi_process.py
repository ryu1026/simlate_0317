import math
from sys import exit
import numpy as np

from main_multi_cell_tracking import do_random_walk, do_triangle
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


# 閾値検出後はすぐに3点計測
# 内部でdo_random_walkも継続しないといけない?
def do_triangle_and_random_walk(col0, row0, col_pos_list, row_pos_list, try_count):
    pos_list_idx = 1
    # 初期座標の格納
    col_pre, row_pre = col0, row0
    trajectory_col_center, trajectory_row_center = [], []
    trajectory_col_center.append(col_pre)
    trajectory_row_center.append(row_pre)
    keikou_threshold = 0.1
    # 3点計測のリスト作成
    col_list, row_list = make_triangle_pos(col_pre_pos=col_pre, row_pre_pos=row_pre)

    print("3点計測開始")
    count = 0
    max_count = 100
    len_over_list_list = []  # over_listの要素数を格納するリスト

    # とりあえずcountの上限を設定して無限ループを避ける
    while count < max_count:
        count += 1
        signal_list = []
        # 3点計測のループ
        for i in range(len(col_list)):
            signal = sim.get_signal_simple(beads_matrix, int(col_list[i]), int(row_list[i]), count)
            signal_list.append(signal)

        over_list = [i for i, x in enumerate(signal_list) if x >= keikou_threshold]
        len_over_list = len(over_list)
        len_over_list_list.append(len_over_list)

        if len_over_list == 0:
            # 完全に座標を特定できたから新しい細胞をdo_random_walkで探索する
            # do_random_walkで探索出来たらそこを中心に3点計測に戻る
            trajectory_row_center.append(row_pre)
            trajectory_col_center.append(col_pre)

            log_triangle(col_center_list=trajectory_col_center[:-1], row_center_list=trajectory_row_center[:-1],
                         len_over_list_list=len_over_list_list, filename=try_count)
            # 閾値を超えた座標が検出されcol_pre, row_preに代入
            col_pre, row_pre = do_random_walk(col0=col_pos_list[pos_list_idx], row0=row_pos_list[pos_list_idx], try_count=3)
            pos_list_idx += 1
            # 3点計測を再びスタート
            col_list, row_list = make_triangle_pos(col_pre_pos=col_pre, row_pre_pos=row_pre)
            # return trajectory_col_center[-1], trajectory_row_center[-1]

        elif len_over_list == 1:
            over_keikou_threshold_x = col_list[over_list[0]]  # 蛍光の閾値 (keikou_threshold) を上回った時のx座標
            over_keikou_threshold_y = row_list[over_list[0]]  # 蛍光の閾値を上回った時のy座標

            col_pre = math.ceil((col_pre + over_keikou_threshold_x) / 2)
            row_pre = math.ceil((row_pre + over_keikou_threshold_y) / 2)
            trajectory_col_center.append(col_pre)
            trajectory_row_center.append(row_pre)

            col_list, row_list = make_triangle_pos(col_pre_pos=col_pre, row_pre_pos=row_pre)
            col_pre, row_pre = do_random_walk(col0=col_pos_list[pos_list_idx], row0=row_pos_list[pos_list_idx], try_count=3, max_count_random_walk=1)

        elif len_over_list == 2:
            over_keikou_threshold_x1, over_keikou_threshold_x2 = col_list[over_list[0]], col_list[over_list[1]]
            over_keikou_threshold_y1, over_keikou_threshold_y2 = row_list[over_list[0]], row_list[over_list[1]]
            col_pre = math.ceil((over_keikou_threshold_x1 + over_keikou_threshold_x2) / 2)
            row_pre = math.ceil((over_keikou_threshold_y1 + over_keikou_threshold_y2) / 2)

            trajectory_col_center.append(col_pre)
            trajectory_row_center.append(row_pre)

            col_list, row_list = make_triangle_pos(col_pre_pos=col_pre, row_pre_pos=row_pre)
            do_random_walk(col0=col_pos_list[pos_list_idx], row0=row_pos_list[pos_list_idx],
                           try_count=3)

        else:
            print("閾値を超えたのが3点 -> triangle_radiusが多分小さすぎる")
            print("いったん終了する")
            break

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

col1, row1 = do_random_walk(col0=int(col_pos_list[0]), row0=int(row_pos_list[0]), try_count=1)
do_triangle_and_random_walk(col0=col1, row0=row1,
                            col_pos_list=col_pos_list, row_pos_list=row_pos_list, try_count=1)
# for j in range(len(col_pos_list)):
#     col1, row1 = do_random_walk(col0=int(col_pos_list[j]), row0=int(row_pos_list[j]), try_count=j + 1)
#     col2, row2 = do_triangle(col0=col1, row0=row1, try_count=j + 1)
