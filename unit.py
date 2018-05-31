import math
from math import sin,cos
import copy
import struct

import numpy as np
import pywavefront
import pywavefront.visualization

from vec import *
import env
import magic
import effect
import particle
import 情形

import time
import 自动

from pythongl import *

from tool import *

def 旋转(a,b):
    a/=np.linalg.norm(a)
    b/=np.linalg.norm(b)
    v=np.cross(a,b)
    d=np.degrees(np.arccos(np.dot(a,b)))
    glRotatef(d,*v)

class 单位():
    生=True
    重力系数=1
    空气阻力系数=0
    形状=vec(1,1,1)
    视高=0
    腿脚速度=2
    跳跃高度=1 #因为积分不满所以实际上达不到
    在走=False
    模型=None
    
    def __init__(self):
        self.id=-1
        self.生命=100
        self.魔力=100
        self.基础速度=vec(0,0,0)
        
        self.位置=vec(0,0,0)
        self.面角=[0,0]
        
        self.法术=h_list(self)
        self.效果=h_list(self)
        
    def __getstate__(self):
        return {0:struct.pack('i10f?',
            self.id,
            self.生命,self.魔力,
            self.基础速度.x,self.基础速度.y,self.基础速度.z,
            self.位置.x,self.位置.y,self.位置.z,
            self.面角[0],self.面角[1],
            self.生
            )}
    def __setstate__(self,state):
        (self.id,
        self.生命,self.魔力,   
        速度x,速度y,速度z,
        位置x,位置y,位置z,
        面角0,面角1,
        self.生) = struct.unpack('i10f?',state[0])
    
        self.基础速度=vec(速度x,速度y,速度z)
        self.位置=vec(位置x,位置y,位置z)
        self.面角=[面角0,面角1]
    
    def tp(self,t):
        self.物理(t)
        
        for i in self.法术:
            i.tp(t)
        for i in self.效果:
            i.tp(t)
        de(self.效果, lambda i: not i.生)
        #233333
        if self.位置.z<-100:
            self.die()
            
    def 物理(self,t): 
        #高度
        self.基础速度.z-=env.G*self.重力系数*t
        if self.空气阻力系数:
            self.基础速度*=(1-self.空气阻力系数)**t
        self.位置.z+=self.速度.z*t
        if self.着地:
            self.基础速度.z=max(0,self.基础速度.z)
            self.位置.z=intt(self.位置.z)+0.999
            if self.基础速度.mo>(4*t):
                self.基础速度-=self.基础速度*(4*t)
            else:
                self.基础速度=vec(0,0,0)
        if self.碰撞:
            self.基础速度.z=min(0,self.基础速度.z)
            
        #水平
        x,y,z=self.位置
        self.位置.x+=self.速度.x*t
        self.位置.y+=self.速度.y*t
        if self.碰撞:
            self.位置.x,self.位置.y=x,y
            self.基础速度.x=0
            self.基础速度.y=0

    @property
    def 中心(self):
        return self.位置+self.形状*0.5

    @property
    def 面向(self):
        a,b=self.面角
        return vec(cos(b)*cos(a),cos(b)*sin(a),sin(b))
        
    @property
    def 行走速度(self):
        v=vec(self.面向.x,self.面向.y,0).normalize()
        return v.adjust_angle(self.行走方向)*self.腿脚速度
    @property
    def 速度(self):
        if self.在走:
            return self.基础速度+self.行走速度
        return self.基础速度
    @property
    def 眼睛(self):
        x,y,z=self.位置
        眼睛=vec(x+self.形状.x/2,y+self.形状.y/2,z+self.视高)
        if self.在走: 
            t=time.clock()*20
            # 眼睛+=vec(sin(t)/70,sin(t+pi/2)/70,sin(t+pi/4)/70)    #视角摇晃
            if self.行走方向==0: 
                眼睛+=self.行走速度*0.015
        return 眼睛
    @property
    def 着地(self):
        return any((i.intize in env.主世界 for i in self.位置.角枚举(self.形状,True)))
        
    @property
    def 碰撞(self):
        return any((i.intize in env.主世界 for i in 
                (self.位置+vec(0,0,0.002)).角枚举(self.形状-vec(0,0,0.004)) 
                ))
    @property
    def 靠墙(self):
        return any((i.intize in env.主世界 for i in
                (self.位置+vec(-0.01,-0.01,0.002)).角枚举(self.形状+vec(+0.02,+0.02,-0.004)) 
                ))
                
    @property
    def 所面向的块(self):
        v1=self.眼睛
        v2=self.面向
        for _ in range(100):
            p=v1.intize
            if p in env.主世界:
                return p
            v1+=v2*0.03
        return None

    def die(self):
        self.生=False
    
    def draw(self):
        if self.模型:
            v=tuple(self.面向)
            with temp_translate(*tuple(self.形状*0.5)):
                旋转(np.array([0,1.,0]),np.array(v))
                self.模型.draw()
                旋转(np.array(v),np.array([0,1.,0]))
            return

        x,y,z=self.形状
        line_box(0,0,0,x,y,z)
        
    def 召唤(self,u,pos=None):
        if callable(u):
            u=u()
        if pos==None:
            u.位置=self.眼睛
        else:
            u.位置=pos
        env.主世界.单位池.加(u)
        
class 虚无:
    def 物理(self,t):     #屏蔽了碰撞等处理
        self.基础速度.z-=env.G*self.重力系数*t
        if self.空气阻力系数:
            self.基础速度*=(1-self.空气阻力系数)**t
        self.位置+=self.速度*t

class 自动的:
    def __init__(self,*l,**d):
        super().__init__(*l,**d)
        self.自动器=self.自动器(self)
    def tp(self,t):
        self.自动器.go(t)
        super().tp(t)

class 炮(虚无,单位):
    重力系数=0.05
    形状=vec(0,0,0)
    def __init__(self):
        super().__init__()
        self.效果.append(effect.限时生命(3))
    def tp(self,t):
        super().tp(t)
        if self.位置.intize in env.主世界:
            self.die()
    def die(self):
        super().die()
        self.召唤(爆炸特效)
    def draw(self):
        with temp_scale(1/8,1/8,1/8):
            with temp_translate(-0.5,-0.5,-0.5):
                gl_list.画gl_list(7)
        
class 箭(虚无,单位):
    空气阻力系数=0.1
    重力系数=0.5
    形状=vec(0,0,0)
    模型=pywavefront.Wavefront('obj/arrow.obj')

    @property
    def 面向(self):
        return self.速度
                
class 球(单位):
    def __init__(self):
        super().__init__()
        self.效果.append(effect.限时生命(15))
    def die(self):
        x,y,z=self.中心
        for i in range(50):
            particle.particle(14,x,y+0.2,z,speed=0.8,t=rd(0.3,1),size=0.2,重力系数=0.1)
        super().die()
    模型=pywavefront.Wavefront('obj/ball.obj')
    形状=vec(0.64,0.64,0.64)

class 魔法球(球):
    def __init__(self,魔法类型):
        super().__init__()
        self.魔法类型=魔法类型
    def 物理(self,t):
        if self.着地:
            魔法=self.魔法类型()
            魔法.owner=self
            魔法.act()
            self.die()
            return
        super().物理(t)

class 插入箭(箭):
    def __init__(self):
        super().__init__()
        self.效果.append(effect.限时生命(15))
    def 物理(self,t):
        if not self.位置.intize in env.主世界:
            super().物理(t)
        
class 反射箭(插入箭):
    def __init__(self):
        super().__init__()
        self.反射次数=4
    def 物理(self,t):
        w=copy.copy(self.位置)
        v=self.基础速度.mo
        super().物理(t)
        反射了=False
        f=16
        while self.反射次数>0 and self.位置.intize in env.主世界:   
            self.位置=w
            self.基础速度=ran_vec()*v
            super().物理(t)
            反射了=True  
            f-=1
            if f<0: break   #我也不知道为什么23333
        if 反射了:
            self.反射次数-=1

class 反射箭弱(反射箭):
    def __init__(self):
        super().__init__()
        self.效果.append(effect.限时生命(6))
        self.反射次数=3
        
class 反射箭强(反射箭):
    def __init__(self):
        super().__init__()
        self.效果.append(effect.限时生命(15))
        self.反射次数=8

class 爆炸特效(虚无,单位):
    重力系数=0
    形状=vec(1,1,1)
    def __init__(self):
        super().__init__()
        self.效果.append(effect.限时生命(0.6))
    def draw(self):
        for _ in range(20):
            x,y,z=rd(-1.0,1.0),rd(-1.0,1.0),rd(-1.0,1.0)
            with temp_translate(x,y,z):
                with temp_scale(1/8,1/8,1/8):
                    gl_list.画gl_list(2)
            
class 圣剑(虚无,单位):
    重力系数=1
    形状=vec(0.2,0.2,1)
    def tp(self,t):
        super().tp(t)
        if self.着地:
            self.die()
    def die(self):
        情形.爆炸(self.位置)
        super().die()
    def draw(self):
        x,y,z=self.位置
        for i in range(3):
            particle.particle(14,x,y,z,speed=0.6,t=rd(0.5,2.5),size=0.3,重力系数=0.1)
            
class 生物(单位):
    def __init__(self):
        super().__init__()
        self.行走方向=0

    def 跳(self):
        if self.着地:
            self.基础速度.z+=math.sqrt(2*env.G*self.重力系数*self.跳跃高度)
            
class 羊(自动的,生物):
    形状=vec(0.4,0.4,0.4)
    自动器=自动.自动走
    腿脚速度=1
    跳跃高度=1.2

class 人(生物):
    视高=1.5
    跳跃高度=1.25
    形状=vec(0.6,0.6,1.8)
    腿脚速度=3
    照片='48035702'
    def __init__(self):
        super().__init__()
        self.法术.append(magic.去块())

        self.法术.append(magic.放块())
        
        self.法术.append(magic.丢球())  #滚轮
        
        self.法术.append(magic.弹幕())  #Q
        self.法术.append(magic.召唤羊())   #E
        self.法术.append(magic.狂热())   #SHIFT

    def draw(self):
        super().draw()
        x,y,z=self.眼睛-self.位置
        
        glTranslatef(x,y,0)
        with points(color=(1,1,1),size=20):
            glVertex3f(0,0,1)
        glRotatef(self.面角[0]/pi*180-90,  0,0,1)
        glTranslatef(-x,-y,0)
        
        glBindTexture(GL_TEXTURE_2D, env.m[self.照片])
        with quads():   
            glTexCoord2f(0, 0)
            glVertex3f(0          , self.形状.y/2, 0)
            glTexCoord2f(0, 1)
            glVertex3f(0          , self.形状.y/2, self.形状.z)
            glTexCoord2f(1, 1)
            glVertex3f(self.形状.x, self.形状.y/2, self.形状.z)
            glTexCoord2f(1, 0)
            glVertex3f(self.形状.x, self.形状.y/2, 0)
        with quads():   
            glTexCoord2f(0, 0)
            glVertex3f(0          , self.形状.y/2, 0)
            glTexCoord2f(1, 0)
            glVertex3f(self.形状.x, self.形状.y/2, 0)
            glTexCoord2f(1, 1)
            glVertex3f(self.形状.x, self.形状.y/2, self.形状.z)
            glTexCoord2f(0, 1)
            glVertex3f(0          , self.形状.y/2, self.形状.z)
        
        glTranslatef(x,y,0)
        glRotatef(-(self.面角[0]/pi*180-90),  0,0,1)
        glTranslatef(-x,-y,0)

    def tp(self,t):
        super().tp(t)
        预加载距离=20
        t=tuple(self.位置+ran_vec()*预加载距离*random.random())
        env.主世界.预生成地形((int(t[0]),int(t[1])))
        
class suin(人):
    照片='48035702'


if __name__=='__main__':
    import pickle
    me=人()
    del me.法术
    del me.效果
    print(len(pickle.dumps(me)))