import math

import env


class 自动器:
    内置cd = 0.1

    def __init__(self, 单位):
        self.单位 = 单位
        self.cd = 0

    def go(self, t):
        self.cd -= t
        if self.cd < 0:
            self.act()
            self.cd += self.内置cd

    def act(self):
        pass


class 自动走(自动器):
    def act(self):
        self.单位.在走 = False
        if self.单位.靠墙:
            self.单位.跳()
        for i, 单位 in env.主世界.单位池.items():
            v = 单位.位置 - self.单位.位置
            if 1 < v.mo < 5:
                self.单位.在走 = True
                self.单位.行走方向 = 0
                self.单位.面角 = [math.acos(v.x / (v.x**2 + v.y**2)**0.5), 0]
                if v.y < 0:
                    self.单位.面角[0] *= -1
                return
