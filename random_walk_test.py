from make_spot_pos import random_walk
import matplotlib.pyplot as plt

col_list, row_list = [], []

col_first = 50
row_first = 50

col_list.append(col_first)
row_list.append(row_first)

for i in range(100):
    col_next, row_next = random_walk(col_first, row_first, scale=5)
    col_list.append(col_next)
    row_list.append(row_next)

for i, (x, y) in enumerate(zip(row_list, col_list)):
    plt.plot(x, y, '-o', label='Point {}'.format(i+1))


plt.title("Scatter plot of beam position")
plt.legend()

plt.show()
