from make_spot_pos import make_triangle_pos, make_triangle_pos_inverse

x_triangle_center = [550, 580, 610, 590, 620, 600, 600]
y_triangle_center = [650, 640, 630, 620, 610, 600, 600]
x_list, y_list = [], []

for i in range(len(x_triangle_center)-1):
    col_list, row_list = make_triangle_pos(y_triangle_center[i], x_triangle_center[i])
    print(col_list)
    for j in range(len(col_list)):
        y_list.append(int(col_list[j]))
        x_list.append(int(row_list[j]))
print("#####")
print(x_list)
print(len(x_list))