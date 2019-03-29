import magic
import block
from pythongl import *


class 物品:
    图标 = ''
    左 = magic.magic
    右 = magic.magic
    shift = magic.magic

    def __init__(self):
        self._owner = None
        self.生 = True
        self.左键技能 = self.左()
        self.右键技能 = self.右()
        self.shift技能 = self.shift()

    @property
    def owner(self):
        return self._owner

    @owner.setter
    def owner(self, owner):
        self._owner = owner
        self.左键技能.owner = owner
        self.右键技能.owner = owner
        self.shift技能.owner = owner

    def 左键开始施法(self):
        self.使用(self.左键技能)

    def 右键开始施法(self):
        self.使用(self.右键技能)

    def 左键停止施法(self):
        self.停止(self.左键技能)

    def 右键停止施法(self):
        self.停止(self.右键技能)

    # def shift使用(self):
    #     self.使用(self.shift技能)

    def 使用(self, 技能):
        技能.call()

    def 停止(self, 技能):
        技能.stop()

    def tp(self, t):
        self.左键技能.tp(t)
        self.右键技能.tp(t)
        self.shift技能.tp(t)

    def die(self):
        self.生 = False

    def __repr__(self):
        return '<物品 %s>' % self.__class__.__name__


class 消耗品(物品):
    可用次数 = 1

    def __init__(self):
        super().__init__()
        self.剩余次数 = self.可用次数

    def 右键开始施法(self):
        print('go')
        super().右键开始施法()
        self.剩余次数 -= 1
        if self.剩余次数 <= 0:
            self.die()

    def __repr__(self):
        return '<物品 %s*%d>' % (self.__class__.__name__, self.剩余次数)


class 手(物品):
    左 = magic.去块


class 弓箭(物品):
    图标 = 'bow'
    左 = magic.去块
    右 = magic.矢散五裂


class 块(消耗品):
    图标 = 'test.png'
    左 = magic.去块
    右 = magic.放块
    id = 0

    def __init__(self):
        super().__init__()
        self.右键技能.块 = block.m[self.id]

    def tex(self, x, y, 面):
        x = x * 16 + 面 * 16
        y = y * 16 + (self.id - 2) * 16
        y = 512 - y
        glTexCoord2f(x / 128.0, y / 512.0)

    @property
    def 图标(self):
        return self.__class__.__name__ + '.png'

    def 绘制(self):
        d = 0.2
        with quads():  # 顶
            self.tex(0, 0, 0)
            glVertex3f(0, 0, d)
            self.tex(0, 1, 0)
            glVertex3f(d, 0, d)
            self.tex(1, 1, 0)
            glVertex3f(d, d, d)
            self.tex(1, 0, 0)
            glVertex3f(0, d, d)
        with quads():  # 底
            self.tex(1, 0, 5)
            glVertex3f(0, 0, 0)
            self.tex(1, 1, 5)
            glVertex3f(0, d, 0)
            self.tex(0, 1, 5)
            glVertex3f(d, d, 0)
            self.tex(0, 0, 5)
            glVertex3f(d, 0, 0)
        with quads():  # 前
            self.tex(1, 1, 1)
            glVertex3f(0, d, 0)
            self.tex(1, 0, 1)
            glVertex3f(0, d, d)
            self.tex(0, 0, 1)
            glVertex3f(d, d, d)
            self.tex(0, 1, 1)
            glVertex3f(d, d, 0)
        with quads():  # 后
            self.tex(0, 1, 2)
            glVertex3f(0, 0, 0)
            self.tex(1, 1, 2)
            glVertex3f(d, 0, 0)
            self.tex(1, 0, 2)
            glVertex3f(d, 0, d)
            self.tex(0, 0, 2)
            glVertex3f(0, 0, d)
        with quads():  # 左
            self.tex(0, 1, 3)
            glVertex3f(d, 0, 0)
            self.tex(1, 1, 3)
            glVertex3f(d, d, 0)
            self.tex(1, 0, 3)
            glVertex3f(d, d, d)
            self.tex(0, 0, 3)
            glVertex3f(d, 0, d)
        with quads():  # 右
            self.tex(1, 1, 4)
            glVertex3f(0, 0, 0)
            self.tex(1, 0, 4)
            glVertex3f(0, 0, d)
            self.tex(0, 0, 4)
            glVertex3f(0, d, d)
            self.tex(0, 1, 4)
            glVertex3f(0, d, 0)


class 沙(块):
    id = 2


class 土(块):
    id = 3


class 草(块):
    id = 4


class 砖(块):
    id = 5


class 橡木板(块):
    id = 6


class TNT(块):
    id = 7


class 钻石(块):
    id = 8


class 石(块):
    id = 9


class 树干(块):
    id = 10


class 叶(块):
    id = 11


class 石台阶(块):
    id = 12


class 石砖(块):
    id = 13


class 雪块(块):
    id = 14


class 红石(块):
    id = 15


class 沙砾(块):
    id = 16


class 金块(块):
    id = 17
