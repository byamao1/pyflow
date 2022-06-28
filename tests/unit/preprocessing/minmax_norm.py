#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/4/20 10:02
# @Author  : Tom


def func(data: dict):
    import numpy as np
    x = data['x']
    y = np.array(data['y'])
    ma = max(y)
    mi = min(y)
    y_out = (y-mi)/(ma-mi)
    return {'x': x, 'y': y_out.tolist()}


if __name__ == '__main__':
    import numpy as np

    data = {'x': np.arange(-3, 0).tolist(), 'y': np.arange(-3, 0).tolist()}
    print(func(data))
