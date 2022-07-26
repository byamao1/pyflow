#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/4/20 10:02
# @Author  : Tom
# https://zhuanlan.zhihu.com/p/31253279

import matplotlib.pyplot as plt
import numpy as np
import pywt
from mpl_toolkits.mplot3d import Axes3D

sampling_rate = 1024
t = np.arange(0, 1.0, 1.0 / sampling_rate)
f1 = 100
f2 = 200
f3 = 300
data = np.piecewise(t, [t < 1, t < 0.8, t < 0.3],
                    [lambda t: np.sin(2 * np.pi * f1 * t), lambda t: np.sin(2 * np.pi * f2 * t),
                     lambda t: np.sin(2 * np.pi * f3 * t)])
wavename = 'cgau8'
totalscal = 256
fc = pywt.central_frequency(wavename)
cparam = 2 * fc * totalscal
scales = cparam / np.arange(totalscal, 1, -1)
[cwtmatr, frequencies] = pywt.cwt(data, scales, wavename, 1.0 / sampling_rate)

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.figure(figsize=(8, 4))
plt.subplot(211)
plt.plot(t, data)
plt.xlabel(u"时间(秒)", )
plt.title(u"300Hz和200Hz和100Hz的分段波形和时频谱", fontsize=20)

fig = plt.figure()
ax = Axes3D(fig)
ax.scatter3D(t, frequencies, abs(cwtmatr), )
# plt.ylabel(u"频率(Hz)", )
# plt.xlabel(u"时间(秒)", )
plt.subplots_adjust(hspace=0.4)
plt.show()
