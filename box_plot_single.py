import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

data_random = [14,	11,	11,	1,	4,	31,	1,	5, 2, 1, 20,	10,	11,	11,	18,	2,	3,	2,	3,	1,	3,	1,	44,	29,	47,	1,	36,	3,
               39,	19,	6,	3,	4,	9,	1,	6,	1,	6,	26,	11,	5,	33,	6,	6,	1,	3,	7,	1,	6,	13]

data_triangle = [9,	10,	9,	10,	9,	18,	4,	6,	7,	11,	27,	5,	6,	10,	10,	15,	20,	21,	5,	6,	8,	14,	20,	9,	15,	10,
                 4 ,4,	8,	9,	5,	20,	2,	20,	20,	5,	10,	9,	19,	2,	13,	12,	15,	9,	2,	6,	4,	4,	2,	6]

data_triangle_after_rest = [6,	10,	5,	4,	6,	23,	4,	13,	13,	20,	9,	2,	20,	4,	20,	15,	8,	5,	10,	11,	20,	25,	5,
                            4,	7,	15,	19,	18,	30,	24,	21,	20,	15,	10,	9,	9,	8,	7,	15,	4,	5,	16,	15,	11,	26,	4,
                            5,	5,	9,	7]

gosa = [1, 1, 1, 1,1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1,
        1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1]

gosa_pd = pd.Series(gosa)
print(gosa_pd.describe())
print(len(gosa))
data_triangle_3 = [i * 3 for i in data_triangle]
data_triangle_after_rest_3 = [i * 3 for i in data_triangle_after_rest]

random_pd = pd.Series(data_random)
data_triangle_3_pd = pd.Series(data_triangle_3)
data_triangle_after_rest_3_pd = pd.Series(data_triangle_after_rest_3)
print(data_triangle_after_rest_3_pd.describe())
# print(np.mean(data))

fig, ax = plt.subplots(figsize=(8, 4))
ax.boxplot(data_triangle_after_rest_3_pd, vert=False, notch=True, patch_artist=True,
           boxprops=dict(facecolor='lightblue', edgecolor='black', linewidth=1.5),
           whiskerprops=dict(color='black', linewidth=1.5),
           capprops=dict(color='black', linewidth=1.5),
           medianprops=dict(color='black', linewidth=2),
           flierprops=dict(marker='o', markerfacecolor='red', markersize=8, alpha=0.7))

ax.set_xlim(0, 100)

# ax.xaxis.label.set_visible(False)
ax.set_xlabel('計測回数 [回]', fontname='MS Gothic', fontsize=18)
# ax.set_title('計測回数の箱ひげ図', fontname='MS Gothic', fontsize=20)

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
ax.set_yticklabels(['3点計測時'], fontname='MS Gothic', fontsize=18)
plt.tight_layout()
plt.show()