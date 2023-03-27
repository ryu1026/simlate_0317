import cv2
from simulation import Simulate
import tifffile
import matplotlib.pyplot as plt
import numpy as np


image = tifffile.imread('initial_beads_2.tiff')
print(image.shape)
print(image.dtype)

fig, ax = plt.subplots()
ax.imshow(image, cmap='gray', interpolation='nearest')
# ax.set_xlabel("x [µm]", fontname='MS Gothic', fontsize=18)
# ax.set_ylabel("y [µm]", fontname='MS Gothic', fontsize=18)
# # ax.set_title("蛍光ビーズ",fontname='MS Gothic', fontsize=20)
# # ax.xaxis.set_ticks_position('top')
# # ax.xaxis.set_label_position('top')
# # ax.invert_yaxis()
# # ax.tick_params(labelbottom=False, labelleft=False, labelright=False, labeltop=False)
ax.axis('off')
# plt.tick_params(labelsize=14)
# plt.tight_layout()
pts = np.array([[500, 500], [540, 490], [570, 450], [590, 480], [600, 550]])
x = [500, 540, 570, 590, 600]
y = [500, 490, 450, 480, 550]
x_2 = [500, 550, 580, 500, 530, 610, 540, 440]
y_2 = [500, 530, 530, 530, 490, 430, 440, 490]
x_0327 = [500, 800, 740, 700, 760, 790, 720, 900, 603, 550]
y_0327 = [500, 620, 810, 630, 790, 700, 540, 690, 570, 650]


for i in range(len(x_0327) - 1):
    ax.plot([x_0327[i], x_0327[i+1]], [y_0327[i], y_0327[i+1]], marker='o', markersize=8, color='red')
    if i == len(x_0327) - 2:
        ax.plot([x_0327[i+1]], [y_0327[i+1]], marker='o', markersize=8, color='red')

plt.tight_layout()
ax.legend().set_visible(False)

plt.show()


