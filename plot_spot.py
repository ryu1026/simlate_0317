from make_spot_pos import make_triangle_pos, make_triangle_pos_inverse
import matplotlib.pyplot as plt

y1,  x1 =  make_triangle_pos(10, 10)
y2, x2 = make_triangle_pos_inverse(10, 10)

plt.scatter(x1, y1)
plt.scatter(x2, y2)
plt.tight_layout()
plt.show()