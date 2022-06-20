#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/4/20 10:02
# @Author  : Tom


def func(file_path, axis_col_map, window_config, loop_n):
    """
    :params: file_path,axis_col_map,window_config,loop_n
    :ptypes: File,Json,Json,Int
    :returns: out
    :rtype: Json
    """
    import os
    import pandas as pd

    # File extension
    ext = os.path.splitext(file_path)[1][1:]
    if ext == 'csv':
        df = pd.read_csv(file_path, header=0)
    elif ext in ['xls', 'xlsx']:
        df = pd.read_excel(file_path, header=0)
    else:
        raise Exception(f"Unsupport file type: [{ext}]")

    offset = loop_n * window_config['shift_len']
    window_len = window_config['window_len']
    if offset + window_len >= len(df):
        return {}
    df = df[offset:offset + window_len]
    df = df.fillna(0)  # Fill nan
    return {k: df[v].tolist() for k, v in axis_col_map.items()}


if __name__ == '__main__':
    file_path = "../data/ts_data.xlsx"
    axis_col_map = {'x': 'id', 'y': 'x'}
    window_config = {"window_len": 1000, "shift_len": 30}
    for i in range(2):
        data = func(file_path, axis_col_map, window_config, loop_n=i)
        print(data)
