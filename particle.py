import math
from math import sin,cos
import random
from tool import *
rdth = lambda: random.random()*2*3.1415926
import env

from pythongl import *
import block
from vec import *

particle_pool=[]

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
    就绪=False
    def __init__(self,方块id,x,y,z,speed,t,size,重力系数=0):
        self.方块id=方块id
        块=block.m[方块id]
        self.纹理 = 块.画底()[0]
        self.x=x
        self.y=y
        self.z=z
        self.size=size
        if isinstance(speed,int) or isinstance(speed,float):
            th1=rdth()
            th2=rdth()
            l=random.random()*speed
            self.speed=[sin(th1)*l*cos(th2),cos(th1)*l*cos(th2),sin(th2)*l]
        else:
            self.speed=list(speed)
        self.t=t
        self.max_time=t
        self.重力系数=重力系数

        if env.启用粒子:
            particle_pool.append(self)
        
        self.a=ran_vec()*self.size
        self.c=ran_vec()*self.size
        self.b=self.a+self.c

        self.a=tuple(self.a)
        self.b=tuple(self.b)
        self.c=tuple(self.c)

        self.就绪=True

    def tp(self,t):
        self.speed[2]-=self.重力系数*env.G*t
        self.t-=t
        if self.t<0:
            particle_pool.remove(self)
            return
        self.x+=self.speed[0]*t
        self.y+=self.speed[1]*t
        self.z+=self.speed[2]*t

    def draw(self):
        if not self.就绪:
            return
        glTranslatef(self.x,self.y,self.z)
        glPointSize(self.size)

        glBegin(GL_QUADS)
        glTexCoord2f(self.纹理[0],self.纹理[1])
        glVertex3f(0,0,0)
        glTexCoord2f(self.纹理[2],self.纹理[3])
        glVertex3f(*self.a)
        glTexCoord2f(self.纹理[4],self.纹理[5])
        glVertex3f(*self.b)
        glTexCoord2f(self.纹理[6],self.纹理[7])
        glVertex3f(*self.c)
        glEnd()

        glTranslatef(-self.x,-self.y,-self.z)
