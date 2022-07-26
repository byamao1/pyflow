#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/4/20 10:02
# @Author  : Tom

def func(data, wavelet):
    import pywt

    x = data['x']
    y = data['y']
    coeffs = pywt.dwt(y, wavelet)
    return coeffs
    # return {'x': np.arange(len(df)).tolist(), 'y': df['X'].tolist()}


if __name__ == '__main__':
    import numpy as np

    data = {'x': np.arange(8).tolist(), 'y': np.random.randint(100, size=(8)).tolist()}

    cA, cD = func(data, 'haar')

    print(cA)
    print(cD)
