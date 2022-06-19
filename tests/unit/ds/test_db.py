#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/4/20 10:02
# @Author  : Tom


def func(db_config, sql, col_axis_map, window_config, loop_n):
    """
    :params: db_config,sql,col_axis_map,window_config,loop_n
    :ptypes: Json,String,Json,Json,Int
    :returns: out
    :rtype: Json
    """
    import pandas as pd
    import pymysql
    # Connect db
    conn = pymysql.connect(host=db_config['host'], port=db_config['port'],
                           user=db_config['user'], passwd=db_config['password'],
                           database=db_config.get('database', None))

    # Execute sql
    sql = f"""
        {sql} LIMIT {window_config['window_len']} OFFSET {loop_n * window_config['shift_len']}
    """
    df = pd.read_sql(sql=sql, con=conn)
    conn.close()
    if len(df) < window_config['window_len']:
        return {}
    return {k: df[v].tolist() for k, v in col_axis_map.items()}


def fft(data: dict):
    import numpy as np
    from scipy.fftpack import fft

    import matplotlib.pyplot as plt
    from matplotlib.pylab import mpl
    mpl.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文
    mpl.rcParams['axes.unicode_minus'] = False  # 显示负号

    x = data['x']
    y = data['y']
    fft_y = fft(y)
    abs_fft = np.abs(fft_y)
    half_x = np.arange(len(x) // 2)
    half_abs_fft = abs_fft[:len(abs_fft) // 2]
    # return {'x': half_x.tolist(), 'y': half_abs_fft.tolist()}
    plt.subplot(231)
    plt.plot(x, y)
    plt.title('原始波形')

    fft_ax = plt.subplot(232)
    # fft_ax.set_yscale('log')
    plt.plot(half_x, half_abs_fft, 'black')
    plt.title('单边振幅谱', fontsize=9, color='black')
    plt.show()


if __name__ == '__main__':
    db_config = {"host": "rm-uf607hj14l5cl21o7fo.mysql.rds.aliyuncs.com",
                 "port": 3306,
                 "user": "aiit_jie",
                 "password": "Aiit-jie-jkwerouioer",
                 "database": "test"
                 }

    sql = "select id, x from ts_data"
    col_axis_map = {'x': 'id', 'y': 'x'}
    window_config = {"window_len": 1000, "shift_len": 30}
    for i in range(10):
        data = func(db_config, sql, col_axis_map, window_config, loop_n=i)
        fft(data)
