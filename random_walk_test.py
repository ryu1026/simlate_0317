from make_spot_pos import random_walk
import matplotlib.pyplot as plt

col_list, row_list = [], []

col_first = 50
row_first = 50

col_list.append(col_first)
row_list.append(row_first)

for i in range(10):
    col_next, row_next = random_walk(col_first, row_first, scale=5)
    col_list.append(col_next)
    row_list.append(row_next)

for i, (x, y) in enumerate(zip(row_list, col_list)):
    plt.plot(x, y, '-o', label='Point {}'.format(i+1))


plt.title("Scatter plot of beam position")
plt.legend()

plt.show()


import random
col_pre = 50
for i in range(10):
    col_pre += np.random.normal(scale=10)
    print(col_pre)
    if col_pre < 10 or col_pre > 90:
        col_pre = np.clip(col_pre, 10, 90)
        print("after_clip", col_pre)