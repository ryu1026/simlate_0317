import pandas as pd


def log_random_walk(random_col_list, random_row_list, random_signal_list, total_num, filename):
    data = {'random_col': random_col_list, 'random_row_list': random_row_list, 'total_move': total_num//3, 'total_num': total_num, 'random_signal': random_signal_list}
    df = pd.DataFrame(data)
    filename = 'random_walk_' + str(filename) + '.xlsx'
    df.to_excel(filename, index=False)


def log_triangle(col_center_list, row_center_list, len_over_list_list, total_num, filename):
    data = {'trajectory_col_center': col_center_list, 'trajectory_row_center': row_center_list, 'total_move': total_num//3, 'total_num': total_num, 'len_over_list': len_over_list_list}
    df = pd.DataFrame(data)
    filename = 'triangle_' + str(filename) + '.xlsx'
    df.to_excel(filename, index=False)
