import numpy as np
from numpy import ndarray


def random_walk(col_pre, row_pre, scale, dist='nom',):
    if dist == 'nom':
        col_pre += np.random.normal(scale)
        row_pre += np.random.normal(scale)
        # スポットを視野のギリギリの部分には作りたくないので範囲を指定する
        #
        if col_pre < 10 or col_pre > 90:
            col_pre = np.clip(col_pre, 10, 90)
        if row_pre < 10 or row_pre > 90:
            row_pre = np.clip(row_pre, 10, 90)
        return int(col_pre), int(row_pre)

    if dist == 'uni':
        x_next = np.random.uniform(0, 100)
        y_next = np.random.uniform(0, 100)

        return x_next, y_next

    if dist == 'int':
        col_pre += np.random.randint(10, 90)
        row_pre += np.random.normal(10, 90)

        if col_pre.min() < 10 or col_pre.max() > 90:
            col_pre: ndarray = np.clip(col_pre, 10, 90)
        if row_pre.min() < 10 or row_pre.max() > 90:
            row_pre: ndarray = np.clip(row_pre, 10, 90)

        return col_pre, row_pre


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

