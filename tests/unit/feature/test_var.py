#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/4/20 10:02
# @Author  : Tom


def func(data: dict):
    import numpy as np
    x = data['x']
    y = data['y']
    out = np.var(y)
    return {'x': x[0], 'y': out}


if __name__ == '__main__':
    import numpy as np

    data = {'x': np.arange(3).tolist(), 'y': np.arange(3).tolist()}
    print(func(data))
