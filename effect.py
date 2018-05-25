import unit
from vec import *

#——————————————————
#基础效果
class effect():
    生=True
    def __init__(self,life_time=99999999):
        self.max_time=life_time
        self.life_time=life_time
    def tp(self,t):
        self.life_time-=t
        if self.life_time<=0:
            self.die()
    def die(self):
        self.生=False
        
class 力(effect):
    def __init__(self,life_time=99999999,force=vec(0,0,0)):
        super().__init__(life_time)
        self.force=force
    def tp(self,t):
        super().tp(t)
        force=self.force
        if callable(self.force):
            force=self.force(self.life_time)
        self.owner.基础速度+=force*t

class 空中力(力):
    def __init__(self,life_time=99999999,force=vec(0,0,0)):
        super().__init__(life_time,force)
        self.force=force
    def tp(self,t):
        super().tp(t)
        if self.owner.着地:
            self.die()
        
class 转圈(effect):
    def tp(self,t):
        super().tp(t)
        self.owner.面角[0]+=15*t
       
class 限时生命(effect):
    def die(self):
        if self.生:
            self.owner.die()
        super().die()