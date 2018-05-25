import env
from pythongl import *

m=dict()

class 块():
    id=1
    坚固=10
    贴图数=6
    @classmethod
    def init(cls):
        起始位置=(cls.id-2)*16
        if cls.贴图数==6:
            cls.顶,cls.底,cls.前,cls.后,cls.左,cls.右=[(i*16,起始位置) for i in range(6)]
        elif cls.贴图数==3:
            cls.顶=(0,起始位置)
            cls.底=(32,起始位置)
            cls.前,cls.后,cls.左,cls.右=[(16,起始位置)]*4
        elif cls.贴图数==1:
            cls.顶,cls.前,cls.后,cls.左,cls.右,cls.底=[(0,起始位置)]*6
        else:
            raise Exception('贴图数量不对')
            
    @classmethod
    def Tex(cls,x,y,面):
        x=面[0]+x*16
        y=面[1]+y*16
        y=512-y
        return x/128,y/512

    @classmethod
    def 画顶(cls):
        return (cls.Tex(0,0,cls.顶)+cls.Tex(0,1,cls.顶)+cls.Tex(1,1,cls.顶)+cls.Tex(1,0,cls.顶)
                ,
                (0, 0, 1,
                 1, 0, 1,
                 1, 1, 1,
                 0, 1, 1))
        
    @classmethod
    def 画底(cls):
        return (cls.Tex(1,0,cls.底)+cls.Tex(1,1,cls.底)+cls.Tex(0,1,cls.底)+cls.Tex(0,0,cls.底)
                ,
                (0, 0, 0,
                 0, 1, 0,
                 1, 1, 0,
                 1, 0, 0))
        
        
    @classmethod
    def 画前(cls):
        return (cls.Tex(1, 1, cls.前)+cls.Tex(1, 0, cls.前)+cls.Tex(0, 0, cls.前)+cls.Tex(0, 1, cls.前)
            ,
            (0, 1, 0,
             0, 1, 1,
             1, 1, 1,
             1, 1, 0))
        
    @classmethod
    def 画后(cls):
        return (
            cls.Tex(0, 1, cls.后)+cls.Tex(1, 1, cls.后)+cls.Tex(1, 0, cls.后)+cls.Tex(0, 0, cls.后)  
            ,
            (0, 0, 0,
             1, 0, 0,
             1, 0, 1,
             0, 0, 1)
            )
        
        
    @classmethod
    def 画左(cls):
        return (
            cls.Tex(0, 1, cls.左)+cls.Tex(1, 1, cls.左)+cls.Tex(1, 0, cls.左)  +cls.Tex(0, 0, cls.左)
            ,
            (1, 0, 0,
             1, 1, 0,
             1, 1, 1, 
             1, 0, 1)
            )
        
    @classmethod
    def 画右(cls):
        return (
            cls.Tex(1, 1, cls.右)+cls.Tex(1, 0, cls.右)+cls.Tex(0, 0, cls.右)+cls.Tex(0, 1, cls.右)
            ,
            (0, 0, 0,
             0, 0, 1,
             0, 1, 1,
             0, 1, 0)
            )
    
class 沙(块):
    贴图数=1
    id=2
    
class 土(块):
    贴图数=1
    id=3
    
class 草(块):
    贴图数=3
    id=4
    
class 砖(块):
    贴图数=1
    texture='brick'
    id=5
    
class 橡木板(块):
    贴图数=1
    texture='oak'
    id=6
    
class TNT(块):
    贴图数=3
    texture='tnt_up','tnt_side','tnt_dn'
    id=7
    
class 钻石(块):
    贴图数=1
    texture='diamond_block'
    id=8

class 石(块):
    贴图数=1
    texture='stone'
    id=9

class 树干(块):
    贴图数=3
    texture='log_oak_top','log_oak','log_oak_top'
    id=10

class 叶(块):
    贴图数=1
    texture='leaves_oak'
    id=11

class 石台阶(块):
    贴图数=3
    texture='leaves_oak'
    id=12

class 石砖(块): 
    贴图数=1
    id=13

class 雪块(块): 
    贴图数=1
    id=14

class 红石(块): 
    贴图数=1
    id=15

class 沙砾(块): 
    贴图数=1
    id=15


for i in 块,沙,土,草,砖,橡木板,TNT,钻石,石,树干,叶,石台阶,石砖,雪块,红石,沙砾:
    m[i.id]=i
    i.init()