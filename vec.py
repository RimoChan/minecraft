import math
from math import sin,cos

from tool import *

import numpy as np

class vec():
    def __init__(self,x,y,z=0):
        self.x=x
        self.y=y
        self.z=z
    def __iter__(self):
        return iter((self.x,self.y,self.z))
    def __add__(self,b):
        return vec(self.x+b.x,self.y+b.y,self.z+b.z)
    def __sub__(self,b):
        return vec(self.x-b.x,self.y-b.y,self.z-b.z)
    def __mul__(self,n):
        return vec(self.x*n,self.y*n,self.z*n)

    def adjust_angle(self,a):   #水平角度调整
        s,c=(sin(a),cos(a))
        return vec( c*self.x-s*self.y , s*self.x+c*self.y ,self.z)

    @property
    def key(self):
        return (self.x+500)*1000000+(self.y+500)*1000+(self.z+500)

    @property
    def intize(self):
        return tuple(intt(i) for i in self)

    @property
    def mo(self):
        return (self.x**2+self.y**2+self.z**2)**0.5

    @property
    def 临近(self):
        x,y,z=self.x,self.y,self.z
        return (x+1,y,z),(x-1,y,z),(x,y+1,z),(x,y-1,z),(x,y,z+1),(x,y,z-1)

    def 同侧(self,v):
        return self.x*v.x+self.y*v.y+self.z*v.z > 0

    def normalize(self):
        if self.mo==0:
            return vec(0,0,1)
        return self*(1/self.mo)
    
    def __str__(self):
        return 'vec(%.2f,%.2f,%.3f)' % tuple(self)
    
    def __repr__(self):
        return 'vec(%.2f,%.2f,%.3f)' % tuple(self)
    
    def ran_dif(self,n):    #随机偏移
        n=float(n)
        return vec(self.x+rd(-n,n),self.y+rd(-n,n),self.z+rd(-n,n))
            
    def 角枚举(self,b,底=False):
        ans=[]
        for x in range(2):
            for y in range(2):
                for z in range(1) if 底 else range(2):
                    ans.append(vec(self.x+x*b.x,self.y+y*b.y,self.z+z*b.z))
        return ans
        
def ran_vec():
    return vec(0,0,0).ran_dif(1).normalize()

if __name__=='__main__':
    v=vec(0,1,2)
    print(v.角枚举(vec(1,1,1)))