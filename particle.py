import math
from math import sin, cos
import random
from tool import *


def rdth(): return random.random() * 2 * 3.1415926


import env

from pythongl import *
import block
from vec import *

particle_pool = []

# def box(x,y,r,func=lambda x,y:None,mult=1):
# if mult<1:
# if random.random()<mult:
# th=rdth()
# r=random.random()*r
# func(x+sin(th)*r,y+cos(th)*r)
# return
# for i in range(mult):
# th=rdth()
# l=random.random()*r
# func(x+sin(th)*l,y+cos(th)*l)


# 速度的三种写法:
# [100,100]速度为x方向100，y方向100
# 100 生成向量在半径为100的圆内的随机速度
# [100] 生成向量在半径为100的圆上的随机速度
class particle():
    就绪 = False

    def __init__(self, 方块id, x, y, z, speed, t, size, 重力系数=0):
        if not env.启用粒子:
            return
        self.方块id = 方块id
        块 = block.m[方块id]
        self.x = x
        self.y = y
        self.z = z
        self.size = size
        if isinstance(speed, int) or isinstance(speed, float):
            th1 = rdth()
            th2 = rdth()
            l = random.random() * speed
            self.speed = [sin(th1) * l * cos(th2), cos(th1) * l * cos(th2), sin(th2) * l]
        else:
            self.speed = list(speed)
        self.t = t
        self.max_time = t
        self.重力系数 = 重力系数

        particle_pool.append(self)

        self.就绪 = True

    def tp(self, t):
        self.speed[2] -= self.重力系数 * env.G * t
        self.t -= t
        if self.t < 0:
            particle_pool.remove(self)
            return
        self.x += self.speed[0] * t
        self.y += self.speed[1] * t
        self.z += self.speed[2] * t

    def draw(self, 视线方向):
        if not self.就绪:
            return
        d = self.size
        with temp_translate(self.x, self.y, self.z):
            with temp_vec_rotate(np.array([0, -1., 0]), np.array(tuple(视线方向))):
                with quads():
                    glVertex3f(0, 0, d)
                    glVertex3f(d, 0, d)
                    glVertex3f(d, 0, 0)
                    glVertex3f(0, 0, 0)
