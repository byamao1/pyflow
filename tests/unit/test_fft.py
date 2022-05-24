#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/4/20 10:02
# @Author  : Tom

def func(a=None):
    import pandas as pd
    import numpy as np

    df = pd.read_csv(r'F:\Projects\Python\jie\pyflow\tests\unit\data/COM6Sensor_Wave1.csv')
    return {'x': np.arange(len(df)).tolist(), 'y': df['X'].tolist()}


def fft(data: dict):
    import numpy as np
    from scipy.fftpack import fft, ifft
    import matplotlib.pyplot as plt
    from matplotlib.pylab import mpl

    mpl.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文
    mpl.rcParams['axes.unicode_minus'] = False  # 显示负号
    x = data['x']
    y = data['y']
    fft_y = fft(y)
    abs_fft = np.abs(fft_y)
    half_x = x[:len(x)//2]
    half_abs_fft = abs_fft[:len(abs_fft)//2]
    # return {'x': half_x, 'y': half_abs_fft.tolist()}
    plt.subplot(231)
    plt.plot(x, y)
    plt.title('原始波形')

    fft_ax = plt.subplot(232)
    # fft_ax.set_yscale('log')
    plt.plot(half_x, half_abs_fft, 'black')
    plt.title('单边振幅谱', fontsize=9, color='black')
    plt.show()


if __name__ == '__main__':
    data = func()
    fft(data)
