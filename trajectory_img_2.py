import cv2
from simulation import Simulate
import tifffile
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from make_spot_pos_2 import make_triangle_pos, make_triangle_pos_inverse


# from cell_tracking_new import shift_beads_matrix

def shift_beads_matrix(beads_matrix, shift_amount):
    shifted_beads_matrix = np.roll(beads_matrix, shift=shift_amount, axis=1)
    return shifted_beads_matrix


image = tifffile.imread('initial_beads_0327.tiff')
move_random_image = shift_beads_matrix(image, 60)
move_image = shift_beads_matrix(image, 110)

print(image.shape)
print(image.dtype)

fig, ax = plt.subplots()
ax.imshow(move_image, cmap='gray', interpolation='nearest')
ax.axis('off')

# pts = np.array([[500, 500], [540, 490], [570, 450], [590, 480], [600, 550]])
# x = [500, 540, 570, 590, 600]
# y = [500, 490, 450, 480, 550]
# x_2 = [500, 550, 580, 500, 530, 610, 540, 440]
# y_2 = [500, 530, 530, 530, 490, 430, 440, 490]

x_random = [500, 580, 810, 200, 100, 670]
y_random = [500, 660, 830, 300, 600, 510]
x_triangle_center = [670, 700, 700, 730, 730]
y_triangle_center = [510, 500, 530, 520, 520]
x_triangle, y_triangle = [], []

# 中心から3点計測の実際の計測点座標を計算する
for i in range(len(x_triangle_center) - 1):
    col_list, row_list = make_triangle_pos(y_triangle_center[i], x_triangle_center[i])
    print(col_list)
    for j in range(len(col_list)):
        y_triangle.append(int(col_list[j]))
        x_triangle.append(int(row_list[j]))

y, x = make_triangle_pos_inverse(y_triangle_center[-1], x_triangle_center[-1])
for k in range(len(y)):
    y_triangle.append(int(y[k]))
    x_triangle.append(int(x[k]))

# ランダムウォークの描画
for i in range(len(x_random) - 1):
    ax.plot([x_random[i], x_random[i + 1]], [y_random[i], y_random[i + 1]], marker='o', markersize=10, color='red',
            label=f'{i + 1}', linewidth=3)
    if i == len(x_random) - 2:
        ax.plot([x_random[i + 1]], [y_random[i + 1]], marker='o', markersize=10, color='red', label=f'{i + 2}', linewidth=3)

for j in range(len(x_triangle) - 1):
    ax.plot([x_triangle[j], x_triangle[j + 1]], [y_triangle[j], y_triangle[j + 1]], marker='o', markersize=10,
            color="orange", linewidth=3)
    if j == len(x_triangle) - 2:
        ax.plot([x_triangle[j + 1]], [y_triangle[j + 1]], marker='o', markersize=10, color='orange', linewidth=3)

# 3点計測の中心の描画
for j in range(len(x_triangle_center) - 1):
    ax.plot([x_triangle_center[j], x_triangle_center[j + 1]], [y_triangle_center[j], y_triangle_center[j + 1]],
            marker='o',
            markersize=8, color="green", linewidth=3)
    if j == len(x_triangle_center) - 2:
        ax.plot([x_triangle_center[j + 1]], [y_triangle_center[j + 1]], marker='o', markersize=10, color='green', linewidth=3)
#
# # 3点計測の実際の計測点の描画


# ax.legend(fontsize=15)
plt.tight_layout()
ax.legend().set_visible(False)

plt.show()
