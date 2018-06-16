import env
from pythongl import *

m=dict()

class 块():
    id=1
    坚固=10

class 沙(块):
    id=2
    
class 土(块):
    id=3
    
class 草(块):
    id=4
    
class 砖(块):
    id=5
    
class 橡木板(块):
    id=6
    
class TNT(块):
    id=7
    
class 钻石(块):
    id=8

class 石(块):
    id=9

class 树干(块):
    id=10

class 叶(块):
    id=11

class 石台阶(块):
    id=12

class 石砖(块): 
    id=13

class 雪块(块): 
    id=14

class 红石(块): 
    id=15

class 沙砾(块): 
    id=16

class 金块(块):
    id=17

import 物品
掉落表={}
掉落表[草]=物品.土
掉落表[叶]=None
def 掉落(id):
    块=m[id]
    if 块 in 掉落表:
        return 掉落表[块]
    return 物品.__dict__[块.__name__]

for i in 块,沙,土,草,砖,橡木板,TNT,钻石,石,树干,叶,石台阶,石砖,雪块,红石,沙砾:
    m[i.id]=i