import 物品
import random


class 物品栏:
    def __init__(self, owner):
        self.owner = owner
        self.空间 = []
        self.选择 = 0
        self.默认物品 = 物品.手()
        self.默认物品.owner = owner
        self.之前物品 = self.默认物品
        
        for _ in range(1000):
            self.加(物品.橡木板())

    @property
    def 当前物品(self):
        if self.选择 < len(self.空间):
            return self.空间[self.选择]
        return self.默认物品

    @property
    def 在用的(self):
        t = self.当前物品
        if t is not self.之前物品:
            self.之前物品.左键停止施法()
            self.之前物品.右键停止施法()
        self.之前物品 = t
        return t

    def 加(self, x):
        if isinstance(x, 物品.消耗品):
            for i in self.空间:
                if type(i) == type(x):
                    i.剩余次数 += 1
                    return
        x.owner = self.owner
        self.空间.append(x)

    def 清理(self):
        self.空间 = [i for i in self.空间 if i.生]

    def 折(self):
        a = []
        for i in self.空间:
            if isinstance(i, 物品.消耗品):
                a.append((i.图标, i.剩余次数))
            else:
                a.append((i.图标, ' '))
        return a

    def tp(self, t):
        # if random.random()<0.05:
        #     print(self.空间,self.在用的)
        for i in self.空间:
            i.tp(t)
        self.默认物品.tp(t)
