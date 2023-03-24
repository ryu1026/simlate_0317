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

# assign different colors to each point
colors = [f'C{i}' for i in range(len(x_2))]

# # plot the data points with different colors
# for i in range(len(x_2)):
#     ax.scatter(x_2[i], y_2[i], color=colors[i], label=f'Point {i}')

for i in range(len(x_2) - 1):
    ax.plot([x_2[i], x_2[i+1]], [y_2[i], y_2[i+1]], marker='o', markersize=8, color=f'C{i}', label=f'{i+1}')
    if i == len(x_2) - 2:
        ax.plot([x_2[i+1]], [y_2[i+1]], marker='o', markersize=8, color=f'C{i+1}', label=f'{i+2}')
# plt.scatter(x_2, y_2, s=10, c='yellow')
# plt.plot(x_2, y_2, marker='o', markersize=6, markerfacecolor='yellow')
ax.legend(fontsize=15)
# ax.legend(fontsize=10, loc='lower center', bbox_to_anchor=(0.5, -0.2), ncol=len(x_2))
plt.tight_layout()
# ax.legend().set_visible(False)

plt.show()


# import matplotlib.pyplot as plt
#
# x_2 = [500, 550, 580, 500, 530, 610, 540, 440]
# y_2 = [500, 530, 530, 530, 490, 430, 440, 490]
#
# # create a figure and axis object with a title
# fig, ax = plt.subplots()
# ax.set_title('Scatter plot of x_2 and y_2')
#
# # plot the data points
# ax.scatter(x_2, y_2)
#
# # add labels for each data point
# for i, txt in enumerate(range(len(x_2))):
#     ax.annotate(txt, (x_2[i], y_2[i]))
#
# # show the plot
# plt.show()

# import matplotlib.pyplot as plt
#
# x_2 = [500, 550, 580, 500, 530, 610, 540, 440]
# y_2 = [500, 530, 530, 530, 490, 430, 440, 490]
#
# # create a figure and axis object with a title
# fig, ax = plt.subplots()
# ax.set_title('Scatter plot of x_2 and y_2')
#
# # assign different colors to each point
# colors = [f'C{i}' for i in range(len(x_2))]
#
# # plot the data points with different colors
# for i in range(len(x_2)):
#     ax.scatter(x_2[i], y_2[i], color=colors[i], label=f'Point {i}')
#
# # add labels for each data point
# # for i, txt in enumerate(range(len(x_2))):
# #     ax.annotate(txt, (x_2[i], y_2[i]))
#
# # add a legend
# ax.legend()
#
# # show the plot
# plt.show()
