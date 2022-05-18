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
    res = np.abs(fft_y)
    # return list(res)
    plt.subplot(231)
    plt.plot(x, y)
    plt.title('原始波形')

    plt.subplot(232)
    plt.plot(x, fft_y, 'black')
    plt.title('双边振幅谱(未求振幅绝对值)', fontsize=9, color='black')
    plt.show()


if __name__ == '__main__':
    data = func()
    fft(data)
