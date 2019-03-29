import block
import unit
import copy
import pickle
import zlib
import threading
import os
import ctypes
import time
import platform

from vec import *
import env
import 块缓冲

if env.客户端:
    import particle

if platform.architecture()[0][:2] == '64':
    c世界 = ctypes.WinDLL('世界.dll')
else:
    c世界 = ctypes.WinDLL('世界32.dll')
c世界.export_vertex.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p]
c世界.have.restype = ctypes.c_bool
c世界.remove_block.restype = ctypes.c_ubyte
c世界.is_new.restype = ctypes.c_bool

下界 = -16
import 物品
import 地形


class 世界():
    def __init__(self):
        self.记录 = []
        self.单位池 = 单位池()
        self.物品池 = 物品池()
        self.delay = []
        self.已初始化区域 = set()
        self.地形生成器 = 地形.地形生成器(种子=233)
        if not env.客户端:
            try:
                self.读取()
            except Exception as e:
                print('读档失败……')

    def __contains__(self, 块座标):
        区域座标 = 块座标[0] // 64, 块座标[1] // 64
        if 区域座标 not in self.已初始化区域:
            while self.地形生成器.生成地形(self, *区域座标):
                if 区域座标 in self.已初始化区域:
                    break
                time.sleep(0.01)
        return c世界.have(*块座标)

    def 预生成地形(self, 块座标):
        if (块座标[0] // 64, 块座标[1] // 64) not in self.已初始化区域:
            t = threading.Thread(target=lambda: self.地形生成器.生成地形(self, 块座标[0] // 64, 块座标[1] // 64))
            t.start()

    def 保存(self):
        data = zlib.compress(pickle.dumps(self.记录))
        try:
            os.mkdir('save_data')
        except:
            None
        with open('save_data/world.dat', 'wb') as f:
            f.write(data)

    def 读取(self):
        with open('save_data/world.dat', 'rb') as f:
            data = f.read()
        self.记录 = pickle.loads(zlib.decompress(data))

        for i in self.记录:
            if i[0] == '放':
                x, y, z, id = i[1], i[2], i[3], i[4]
                self.放块(x, y, z, block.m[id], 初=True)
            elif i[0] == '去':
                x, y, z = i[1], i[2], i[3]
                self.去块(x, y, z, 初=True)

    def 放块(self, x, y, z, 块, 远程=False, 初=False):
        if not env.客户端 and not 初:
            self.记录.append(('放', x, y, z, 块.id))
        if env.客户端 and not 初 and not 远程:
            return
        c世界.set_block(x, y, z, 块.id)

    def 去块(self, x, y, z, 远程=False, 初=False):
        if not env.客户端 and not 初:
            self.记录.append(('去', x, y, z))

        if env.客户端 and not 远程 and not 初:
            return

        if (x, y, z) not in self:  # 防止线程冲突
            return

        块 = c世界.remove_block(x, y, z)

        if not env.客户端 and not 初 and 块:
            物品 = block.掉落(块)
            if 物品:
                self.物品池.加(((x + 0.5, y + 0.5, z), 物品()))

        if env.客户端 and env.启用粒子 and not 初:
            for i in range(30):
                particle.particle(块, x + rd(0.1, 0.9), y + rd(0.1, 0.9), z + rd(0.1, 0.9), speed=4, t=rd(0.2, 0.4), size=0.1, 重力系数=0.6)

    def 是最新(self, m):
        return c世界.is_new(*m)

    def tp(self, t):
        池 = copy.copy(self.单位池)
        for i in 池:
            self.单位池[i].tp(t)

        for i in 池:
            if not 池[i].生:
                self.单位池.pop(i)
        for u in self.单位池.lazy:
            self.单位池[u.id] = u
        self.单位池.lazy = []

        for i in self.delay:
            i[0] -= t
            if i[0] < 0:
                i[1]()
                self.delay.remove(i)


class 物品池(dict):
    n = 0

    def 加(self, u):
        assert isinstance(u, tuple)
        self[self.n] = u
        self.n += 1


class 单位池(dict):
    n = 0

    def __init__(self):
        self.lazy = []

    def 加(self, u):
        if callable(u):
            u = u()
        u.id = self.n
        self.lazy.append(u)
        self.n += 1


def test():
    a = 世界()
    print((-1, -1) in a)
    print((0, 0) in a)
    print((-1, 0) in a)
    print((0, -1) in a)


if __name__ == '__main__':
    import cProfile

    cProfile.run("test()", "result")

    import pstats
    p = pstats.Stats("result")

    p.strip_dirs().sort_stats("tottime").print_stats()
