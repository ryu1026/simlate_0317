import matplotlib.pyplot as plt

# # 点と点は結ばれていない
# x_2 = [500, 550, 580, 500, 530, 610, 540, 440]
# y_2 = [500, 530, 530, 530, 490, 430, 440, 490]
#
# # create a figure and axis object with a title
# fig, ax = plt.subplots()
# ax.set_title('Line graph of x_2 and y_2 with colored markers')
#
# # plot the line graph with colored markers
# for i in range(len(x_2)):
#     ax.plot([x_2[i]], [y_2[i]], marker='o', markersize=10, color=f'C{i}', label=f'Point {i}')
#
# # add labels for each data point
# for i, txt in enumerate(range(len(x_2))):
#     ax.annotate(txt, (x_2[i], y_2[i]))
#
# # add a legend
# ax.legend()
#
# # show the plot
# plt.show()
#
# # 点と点が線で結ばれている
# x_2 = [500, 550, 580, 500, 530, 610, 540, 440]
# y_2 = [500, 530, 530, 530, 490, 430, 440, 490]
#
# # create a figure and axis object with a title
# fig, ax = plt.subplots()
# ax.set_title('Line graph of x_2 and y_2 with colored markers and connecting lines')
#
# # plot the line graph with colored markers and connecting lines
# for i in range(len(x_2) - 1):
#     ax.plot([x_2[i], x_2[i+1]], [y_2[i], y_2[i+1]], marker='o', markersize=10, color=f'C{i}', label=f'Point {i}')
#     if i == len(x_2) - 2:
#         ax.plot([x_2[i+1]], [y_2[i+1]], marker='o', markersize=10, color=f'C{i+1}', label=f'Point {i+1}')
#
# # add labels for each data point
# for i, txt in enumerate(range(len(x_2))):
#     ax.annotate(txt, (x_2[i], y_2[i]))
#
# # add a legend
# ax.legend()
#
# # show the plot
# plt.show()

import matplotlib.pyplot as plt

x_2 = [500, 550, 580, 500, 530, 610, 540, 440]
y_2 = [500, 530, 530, 530, 490, 430, 440, 490]

# create a figure and axis object with a title
fig, ax = plt.subplots()
ax.set_title('Line graph of x_2 and y_2 with colored markers and connecting lines')

# plot the line graph with colored markers and a single color for the connecting lines
for i in range(len(x_2) - 1):
    ax.plot([x_2[i], x_2[i+1]], [y_2[i], y_2[i+1]], marker='o', markersize=10, color=f'C{i}', label=f'Point {i}', linestyle='-', linewidth=2, zorder=1)
    if i == len(x_2) - 2:
        ax.plot([x_2[i+1]], [y_2[i+1]], marker='o', markersize=10, color=f'C{i+1}', label=f'Point {i+1}', linestyle='-', linewidth=2, zorder=1)

# add labels for each data point
for i, txt in enumerate(range(len(x_2))):
    ax.annotate(txt, (x_2[i], y_2[i]))

# add a legend
ax.legend()

# show the plot
plt.show()

