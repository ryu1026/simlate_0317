import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

data_random = [14,	11,	11,	1,	4,	31,	1,	5, 2, 1, 20,	10,	11,	11,	18,	2,	3,	2,	3,	1,	3,	1,	44,	29,	47,	1,	36,	3,
               39,	19,	6,	3,	4,	9,	1,	6,	1,	6,	26,	11,	5,	33,	6,	6,	1,	3,	7,	1,	6,	13]

data_triangle = [4,	3,	3,	1,	1,	3,	3,	5,	8,	8,	4,	8,	1,	1,	5,	7,	1,	2,	5,	6,	2,	1,	3,	6,	6,	7,
                 5,	4,	2,	10,	1,	1,	2,	3,	5,	8,	5,	4,	4,	5,	6,	2,	6,	9,	1,	6,	4,	4,	1,	6]

data_triangle_after_rest = [5,	10,	5,	6,	4,	4,	1,	7,	10,	4,	3,	4,	1,	1,	3,	5,	7,	5,	4,	4,	6,	5,	5,
                            4,	1,	4,	4,	1,	3,	4,	1,	8,	5,	1,	4,	6,	5,	5,	5,	1,	5,	6,	1,	1,	6,	4,
                            5,	5,	1,	1]
data_triangle_3 = [i * 3 for i in data_triangle]
data_triangle_after_rest_3 = [i * 3 for i in data_triangle_after_rest]

random_pd = pd.Series(data_random)
data_triangle_3_pd = pd.Series(data_triangle_3)
data_triangle_after_rest_3_pd = pd.Series(data_triangle_after_rest_3)
print(data_triangle_after_rest_3_pd.describe())
# print(np.mean(data))

fig, ax = plt.subplots(figsize=(8, 4))
ax.boxplot(data_random, vert=False, notch=True, patch_artist=True,
           boxprops=dict(facecolor='lightblue', edgecolor='black', linewidth=1.5),
           whiskerprops=dict(color='black', linewidth=1.5),
           capprops=dict(color='black', linewidth=1.5),
           medianprops=dict(color='black', linewidth=2),
           flierprops=dict(marker='o', markerfacecolor='red', markersize=8, alpha=0.7))

ax.set_xlim(0, 50)

# ax.xaxis.label.set_visible(False)
ax.set_xlabel('計測回数 [回]', fontname='MS Gothic', fontsize=18)
ax.set_title('計測回数の箱ひげ図', fontname='MS Gothic', fontsize=20)

# Set the background color of the plot
ax.set_facecolor('#f7f7f7')

# Add gridlines to the plot
ax.grid(axis='y', linestyle='-', alpha=0.2)
# ax.set_xticklabels([])
ax.tick_params(labelbottom=True, labelleft=True, labelright=False, labeltop=False)
# ax.spines['bottom'].set_visible(False)
# Show the plot
#
plt.tick_params(labelsize=18)
ax.set_yticklabels(['ランダム時'], fontname='MS Gothic', fontsize=18)
plt.tight_layout()
plt.show()