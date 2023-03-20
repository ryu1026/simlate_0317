import numpy as np
from numpy import ndarray


def random_walk(col_pre, row_pre, scale=5, scale_factor=3, dist='nom'):
    if dist == 'nom':
        col_pre += np.random.normal(scale=scale)
        row_pre += np.random.normal(scale=scale)
        # スポットを視野のギリギリの部分には作りたくないので範囲を指定する
        #
        if col_pre < 10:
            col_pre += abs(np.random.normal(scale=scale*scale_factor))
        elif col_pre > 90:
            col_pre -= abs(np.random.normal(scale=scale*scale_factor))
        else:
            pass

        col_pre = np.clip(col_pre, 10, 90)

        if row_pre < 10:
            row_pre += abs(np.random.normal(scale=scale*scale_factor))
        elif row_pre > 90:
            row_pre -= abs(np.random.normal(scale=scale*scale_factor))
        else:
            pass

        row_pre = np.clip(row_pre, 10, 90)

        return int(col_pre), int(row_pre)

    if dist == 'uni':
        x_next = np.random.uniform(0, 100)
        y_next = np.random.uniform(0, 100)

        return x_next, y_next

    # if dist == 'int':
    #     col_pre += np.random.randint(10, 90)
    #     row_pre += np.random.normal(10, 90)
    #
    #     if col_pre.min() < 10 or col_pre.max() > 90:
    #         col_pre: ndarray = np.clip(col_pre, 10, 90)
    #     if row_pre.min() < 10 or row_pre.max() > 90:
    #         row_pre: ndarray = np.clip(row_pre, 10, 90)

        return col_pre, row_pre


def make_triangle_pos(col_pre_pos, row_pre_pos, triangle_radius=6, do_print=False):
    """
    閾値を上回った座標を中心とした3点の座標

    :param do_print: 中心座標を表示するかどうか
    :param col_pre_pos: 前の集光点のy座標
    :param row_pre_pos: 前の集光点のx座標
    :param triangle_radius: 3点計測 (三角形) の外接円の半径

    :return:　x_list, y_list
    """
    col_list = []
    row_list = []
    # 閾値を上回った座標を中心に3点
    if do_print:
        print("集光中心:({0}, {1}) = (行, 列)".format(col_pre_pos, row_pre_pos))
    for i in range(0, 3):
        col = col_pre_pos + triangle_radius * np.cos(2 * i * np.pi / 3)
        row = row_pre_pos + triangle_radius * np.sin(2 * i * np.pi / 3)
        col_list.append(col)
        row_list.append(row)
    return col_list, row_list


def log_signal_spot(col_list, row_list, trajectory_col, trajectory_row):
    for i in range(len(col_list)):
        trajectory_col.append(col_list[i])
        trajectory_row.append(row_list[i])
    return trajectory_col, trajectory_row
