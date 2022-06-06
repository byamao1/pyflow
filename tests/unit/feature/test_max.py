#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/4/20 10:02
# @Author  : Tom
import matplotlib.pyplot as plt

def func(data: dict):
    x = data['x']
    y = data['y']
    y_max = max(y)
    plt.plot(x, y)
    plt.show()
    return {'x': x[0], 'y': y_max}



if __name__ == '__main__':
    import numpy as np
    data = {'x': np.arange(10).tolist(), 'y': np.arange(10).tolist()}

    print(func(data))
