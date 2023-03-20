import pandas as pd


def log_random_walk(random_col_list, random_row_list, random_signal_list):
    data = {'random_col': random_col_list, 'random_row_list': random_row_list, 'random_signal': random_signal_list}
    df = pd.DataFrame(data)
    df.to_excel('trajectory_random_walk.xlsx', index=False)


def log_csv(col_center_list, row_center_list, len_over_list_list):
    data = {'trajectory_col_center': col_center_list, 'trajectory_row_center': row_center_list, 'len_over_list': len_over_list_list}
    df = pd.DataFrame(data)
    df.to_excel('trajectory_center.xlsx', index=False)
