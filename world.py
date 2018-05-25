import block
import unit
import copy
import pickle
import zlib
import threading

from vec import *
import env
import 块缓冲

if env.客户端:
    import particle

import 地形
class 世界():
    def __init__(self):
        self.全块={}
        self.亮度={}
        self.顶={}
        self.块索引={}
        self.记录=[]
        self.单位池=单位池()
        self.delay=[]
        self.已初始化区域=set()
        self.地形生成器=地形.地形生成器(种子=233)
        if not env.客户端:
            try:
                self.读取()
            except:
                print('读档失败……')

    def __contains__(self,块座标):
        if (块座标[0]//64,块座标[1]//64) not in self.已初始化区域:
            while self.地形生成器.生成地形(self,块座标[0]//64,块座标[1]//64):
                233
        if 块座标 in self.全块:
            return True

    def 预生成地形(self,块座标):
        if (块座标[0]//64,块座标[1]//64) not in self.已初始化区域:
            t = threading.Thread(target=lambda:self.地形生成器.生成地形(self,块座标[0]//64,块座标[1]//64))
            t.start()
        
    def 保存(self):
        data=[]
        for pos,块 in self.全块.items():
            x,y,z=pos
            data.append((x,y,z,块.id))
        data=zlib.compress(pickle.dumps(data))
        f=open('save_data/world.dat','wb')
        f.write(data)
        f.close()
    def 读取(self):
        f=open('save_data/world.dat','rb')
        data=f.read()
        f.close()
        data=pickle.loads(zlib.decompress(data))
        for i in data:
            x,y,z,id=i[0],i[1],i[2],i[3]
            self.放块(x,y,z,block.m[id])
        
    def 放块(self,x,y,z,块,强制=False,初=False):
        self.去块(x,y,z,初=初)
        # print('放',(x,y,z))
        if self.顶.get((x,y),-16)<z:
            self.顶[x,y]=z
        
        if not env.客户端 and not 初:
            self.记录.append(('放',x,y,z,块.id))
        if env.客户端 and not 强制 and not 初:
            return

        self.全块[x,y,z]=块.id

        m=x//16,y//16,z//16
        索引=self.块索引.setdefault(m,[])
        索引.append((x,y,z))

        self.亮度[x,y,z]=0
        self.更新周边亮度(x,y,z)

        if not 初:
            self.绘图重置(x,y,z)

    def 更新亮度(self,x,y,z):
        if not -16<z<128: return
        if (x,y,z) in self.全块: 
            return

        if self.顶.get((x,y),-16)<z:
            t=15
        else:
            a=self.亮度.get((x,y,z+1), 15)
            b=self.亮度.get((x,y,z-1), 15)
            c=self.亮度.get((x,y+1,z), 15)
            d=self.亮度.get((x,y-1,z), 15)
            e=self.亮度.get((x+1,y,z), 15)
            f=self.亮度.get((x-1,y,z), 15)
            t=max(0,max(a,b,c,d,e,f)-1)
        亮度=self.亮度.get((x,y,z), 15)
        if 亮度!=t:
            self.亮度[x,y,z]=t
            self.更新周边亮度(x,y,z)
            self.绘图重置(x,y,z)

    def 更新周边亮度(self,x,y,z):
        self.更新亮度(x,y,z+1)
        self.更新亮度(x,y,z-1)
        self.更新亮度(x,y+1,z)
        self.更新亮度(x,y-1,z)
        self.更新亮度(x+1,y,z)
        self.更新亮度(x-1,y,z)


    def 去块(self,x,y,z,强制=False,初=False):
        if (x,y,z) not in self:
            return
        
        if not env.客户端 and not 初:
            self.记录.append(('去',x,y,z))
            
        if env.客户端 and not 强制 and not 初:
            return
        if env.客户端 and env.启用粒子 and not 初:
            for i in range(20):
                particle.particle(self.全块[(x,y,z)] ,x+rd(0.0,1.0),y+rd(0.0,1.0),z+rd(0.0,1.0)
                    ,speed=0.3,t=rd(0.2,0.9),size=0.1,重力系数=0.1)
        
        self.绘图重置(x,y,z)
        # print(x,y,z)
        self.全块.pop((x,y,z))
        self.块索引[x//16,y//16,z//16].remove((x,y,z))

        if self.顶.get((x,y),-16)==z:
            self.更新顶(x,y)
        self.更新亮度(x,y,z)

    def 更新顶(self,x,y):
        顶=self.顶.setdefault((x,y),-16)
        for i in range(顶,-16,-1):
            if (x,y,i) in self.全块:
                self.顶[x,y]=i
                break

    def 绘图重置(self,x,y,z):
        for v in vec(x,y,z).临近:
            m=v[0]//16,v[1]//16,v[2]//16
            if m in 块缓冲.数据字典:
                块缓冲.数据字典[m]['可用']=False

    def tp(self,t):
        池=copy.copy(self.单位池)
        for i in 池:
            self.单位池[i].tp(t)
        
        for i in 池:
            if not 池[i].生:
                self.单位池.pop(i)
        for u in self.单位池.lazy:
            self.单位池[u.id]=u
        self.单位池.lazy=[]
        
        for i in self.delay:
            i[0]-=t
            if i[0]<0:
                i[1]()
                self.delay.remove(i)
        
class 单位池(dict):
    n=0
    def __init__(self):
        self.lazy=[]
    def 加(self,u):
        if callable(u):
            u=u()
        u.id=self.n
        self.lazy.append(u)
        self.n+=1
    def 缩减(self):
        池=copy.copy(self)
        for i in 池:
            池[i]=copy.copy(池[i])
            del 池[i].法术
            del 池[i].效果
            池[i].位置=(池[i].位置*1000).intize
            池[i].基础速度=(池[i].基础速度*1000).intize
        return 池
    def 展开(self):
        池=copy.copy(self)
        for i in 池:
            池[i]=copy.copy(池[i])
            池[i].位置=vec(*池[i].位置)*0.001
            池[i].法术=()
            池[i].效果=()
            池[i].基础速度=vec(*池[i].基础速度)*0.001
        return 池
        
if __name__=='__main__': 
    a=世界()
    print((0,0) in a)
    print((-1,-1) in a)
    print((-1,0) in a)
    print((0,-1) in a)