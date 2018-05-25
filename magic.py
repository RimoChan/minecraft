from vec import *
import unit
import effect
import env
import block
import 情形

class magic():
    cool_down=5        #冷却时间
    cool_down_left=0   #当前冷却时间
    
    def call(self):
        if self.cool_down_left:
            return
        self.cool_down_left=self.cool_down
        self.act()
    
    #只有持续施法需要stop
    def stop(self):
        None
            
    def tp(self,t):
        self.cool_down_left-=t
        if self.cool_down_left<0:
            self.cool_down_left=0
            
    def act(self):
        pass

class 持续法术(magic):
    内置cd=0
    def __init__(self):
        super().__init__()
        self.施法中=False
        self.cd=0

    def call(self):
        if self.cool_down_left:
            return
        self.cool_down_left=self.cool_down
        self.施法中=True
        self.起动效果()
        self.持续动作(0)

    def stop(self):
        if not self.施法中: 
            return
        self.施法中=False
        self.停止效果()

    def 起动效果(self):
        pass
    def 停止效果(self):
        pass

    def tp(self,t):
        super().tp(t)
        if not self.施法中:
            return
        if self.内置cd:
            self.cd-=t
            if self.cd<=0:
                self.持续动作(self.内置cd)
                self.cd+=self.内置cd
        else:
            self.持续动作(t)

    def 持续动作(self,t):
        None

class 自己爆炸(magic):
    cool_down=0.1
    def act(self):
        情形.爆炸(self.owner.位置)
        
class 开炮(magic):
    cool_down=1    
    def act(self):
        p=unit.炮()
        p.基础速度=self.owner.面向*35
        self.owner.召唤(p)

class 丢球(magic):
    cool_down=0.1
    def act(self):
        # p=unit.魔法球(裁人的圣剑)
        # p=unit.魔法球(射箭)
        # p=unit.魔法球(自己爆炸)
        p=unit.魔法球(冰盾)
        p.基础速度=self.owner.面向*20
        self.owner.召唤(p)
        
class 冰盾(magic):
    cool_down=10
    def act(self):
        c=self.owner.中心
        for i in range(-3,4):
            for j in range(-3,4):
                for k in range(-3,4):
                    if i in (-3,3) or j in (-3,3) or k in (-3,3):
                        t=c+vec(i,j,k) 
                        if t.intize not in env.主世界: 
                            env.主世界.放块(*t.intize,block.雪块)

class 放块(magic):
    cool_down=0.1
    def act(self):
        v0=self.owner.眼睛
        v1=self.owner.眼睛
        v2=self.owner.面向
        for _ in range(600):
            if v1.intize in env.主世界: 
                env.主世界.放块(*v0.intize,block.红石)
                return
            v0=v1
            v1+=v2*0.01
        
class 去块(持续法术):
    cool_down=0
    内置cd=0.04
    目标=None
    def stop(self):
        super().stop()
        self.计时=0

    def 持续动作(self,t):
        v1=self.owner.眼睛
        v2=self.owner.面向
        for _ in range(100):
            p=v1.intize
            if p in env.主世界:
                if p==self.目标:
                    self.计时+=t
                else: 
                    self.目标=p
                    self.计时=0
                if self.计时>0.8:
                    env.主世界.去块(*p)
                    self.目标=None
                    self.计时=0
                break
            else:
                v1+=v2*0.03

class 狂热(持续法术): 
    cool_down=0
    def 起动效果(self):
        print(self.owner.腿脚速度)
        self.owner.腿脚速度*=2

    def 停止效果(self):
        print(self.owner.腿脚速度)
        self.owner.腿脚速度/=2

class 持续射箭(持续法术):
    内置cd=0.2
    cool_down=0.3
    def 持续动作(self,t):
        p=unit.反射箭强()
        p.基础速度=self.owner.面向*30
        self.owner.召唤(p)

class 蓄力射箭(持续法术):
    cool_down=0.3
    def __init__(self):
        self.计时=0
        super().__init__()

    def 停止效果(self):
        p=unit.插入箭()
        p.基础速度=self.owner.面向*30*max(0.1,min(4,self.计时))
        self.owner.召唤(p)
        self.计时=0
        
    def 持续动作(self,t):
        self.计时+=t
        
class 矢散五裂(magic):
    cool_down=0.1
    def act(self):
        for _ in range(10):
            p=unit.反射箭弱()
            p.基础速度=self.owner.面向*30
            self.owner.召唤(p)
    
class 弹幕(magic):
    cool_down=10
    def act(self):
        for i in range(20):
            def t(): 
                p=unit.插入箭()
                p.基础速度=(self.owner.面向*40).ran_dif(2)
                self.owner.召唤(p,pos=self.owner.眼睛.ran_dif(0.5))
            env.主世界.delay.append([0.1*i,t])

class 喷气背包(magic):
    cool_down=10
    def act(self):
        self.owner.效果.append(effect.空中力(5.2,lambda t:vec(0,0,19.6)*((5.2-t)/5.2) ))
        self.owner.基础速度.z=17
        
class 剑刃风暴(magic):
    cool_down=6
    def act(self):
        self.owner.效果.append(effect.转圈(3))
    
class 裁人的圣剑(magic):
    cool_down=6
    def act(self):
        p=unit.圣剑()
        self.owner.召唤(p)
        p.位置.z+=20
        p.基础速度.z+=2.5
    
    