import functools
import time

import cv2
import numpy as np
import random

import block
import clock


def 哈希(x):
    if x >= 0:
        return x * 2
    else:
        return -2 * x - 1


class 地形生成器:
    def __init__(self, 种子):
        self.种子 = 种子
        self.迭代 = 6
        self.块边长 = 2**self.迭代
        self.锁 = False

    def 适应种子(self, x, y):
        return int('%d%d%d' % (哈希(x), self.种子, 哈希(y)))

    @functools.lru_cache(100)
    def 原矩阵(self, 块x, 块y):
        R = random.Random(self.适应种子(块x, 块y))
        rd = R.randint

        a = np.float32([[0]])

        for i in range(self.迭代):
            for j in range(2**i * 2**i):
                a[rd(0, 2**i - 1), rd(0, 2**i - 1)] += (R.random() - 1) / (i + 3) * 16
            a = cv2.resize(a, (2**(i + 1), 2**(i + 1)))
        return a

    def 生成矩阵(self, 块x, 块y):
        l = self.块边长

        al = np.zeros((l * 3, l * 3))
        for x in range(0, 3):
            for y in range(0, 3):
                al[l * x:l * (x + 1), l * y:l * (y + 1)] = self.原矩阵(块x + x - 1, 块y + y - 1)

        al = cv2.GaussianBlur(al, (11, 11), 0)

        return al[l:l * 2, l:l * 2].astype(int)

    def 放树(self, 世界, x, y, z):
        for i in range(1, 5):
            世界.放块(x, y, z + i, block.树干, 初=True)
        for dx in range(-3, 4):
            for dy in range(-3, 4):
                for dz in range(4, 8):
                    if dx**2 + dy**2 + (dz - 4)**2 < 14:
                        世界.放块(x + dx, y + dy, z + dz, block.叶, 初=True)

    def 生成地形(self, 世界, 块x, 块y):
        if self.锁:
            return True
        self.锁 = True
        assert (块x, 块y) not in 世界.已初始化区域
        print('初始化:', 块x, 块y, '……')
        c = clock.clock()
        c.tick()

        世界.已初始化区域.add((块x, 块y))

        下界 = -16
        a = self.生成矩阵(块x, 块y)
        for 相对x in range(0, self.块边长):
            for 相对y in range(0, self.块边长):
                z = int(a[相对x, 相对y])
                x = 相对x + self.块边长 * 块x
                y = 相对y + self.块边长 * 块y
                for zt in range(下界, z - 3):
                    世界.放块(x, y, zt, block.石, 初=True)
                for zt in range(z - 3, z):
                    世界.放块(x, y, zt, block.土, 初=True)
                世界.放块(x, y, z, block.草, 初=True)

        R = random.Random(self.适应种子(块x, 块y))
        for _ in range(15):
            相对位置 = R.randint(4, self.块边长 - 5), R.randint(4, self.块边长 - 5)
            位置 = 相对位置[0] + self.块边长 * 块x, 相对位置[1] + self.块边长 * 块y
            self.放树(世界, *位置, int(a[相对位置]))

        print('用时%.3fs。' % c.tick())
        self.锁 = False

        return False
