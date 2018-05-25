import threading
import time
import random
import math
import sys
import copy

import numpy 

from pythongl import *

import particle
import 块缓冲
from math import sin,cos

from tool import *

from vec import *

import clock

import env
env.客户端=True
import world
env.主世界=world.世界()

import net_client
import block
import particle
import unit
import env
import block

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from 配置 import 配置

class 主窗口(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon('图/圖標.ico'))
        self.resize(*配置.屏幕大小)
        self.setWindowTitle("卖淫先锋")
        self.glWidget = GLWidget(self)
        self.提示=QLabel(self)
        self.提示.resize(200,80)
        self.无控制遮罩=QLabel(self)
        self.无控制遮罩.resize(*配置.屏幕大小)
        self.无控制遮罩.setStyleSheet("background-color:rgba(0,0,0,0.5);")
        self.控制接上()
        
        if 配置.surface模式:
            self.p0=None
            self.所有触点=[]
        
            self.setAttribute(Qt.WA_AcceptTouchEvents, True)
            QCoreApplication.setAttribute(Qt.AA_SynthesizeTouchForUnhandledMouseEvents, True)
            QCoreApplication.setAttribute(Qt.AA_SynthesizeMouseForUnhandledTouchEvents, True)
        
            self.控制球=QLabel(self)
            self.控制球.resize(配置.控制球大小,配置.控制球大小)
            self.控制球.move(50,配置.屏幕大小[1]-配置.控制球大小-50)
            self.球图=QPixmap('./图/球.png')
            self.控制球.setPixmap(self.球图)
            self.控制球.setScaledContents(True)

    def eventFilter(self,  source,  event):
        if event.type() == QEvent.WindowDeactivate:
            self.控制断开()
        if 配置.surface模式:
            if event.type() == QEvent.TouchBegin:
                pass
            if event.type() == QEvent.TouchUpdate:
                self.所有触点=[]
                self.glWidget.控制=[0,0]
                for i,触点 in enumerate(event.touchPoints()):
                    p0=触点.pos()
                    p1=触点.lastPos()
                    self.触摸屏拖动(p0.x(),p0.y(),p1.x(),p1.y())
                    self.球动(p0.x(),p0.y(),p1.x(),p1.y())
            if event.type() == QEvent.TouchEnd:
                self.所有触点=None
                self.glWidget.控制=[0,0]
                
        return False

    def mousePressEvent(self, event):
        if not self.glWidget.接管鼠标:
            self.控制接上()
            return

        if 配置.surface模式:
            return

        if event.button() == Qt.LeftButton: 
            net_client.udp_send(('法术',0,'开始施法'))
        if event.button() == Qt.RightButton: 
            net_client.udp_send(('法术',1,'开始施法'))

    def mouseReleaseEvent(self,event):
        if 配置.surface模式:
            return

        if event.button() == Qt.LeftButton: 
            net_client.udp_send(('法术',0,'停止施法'))
        if event.button() == Qt.RightButton: 
            net_client.udp_send(('法术',1,'停止施法'))
        if 配置.surface模式:
            self.p0 = None

    def 触摸屏拖动(self,x0,y0,x1,y1):
        t = vec(x0,y0) - vec(x1,y1)
        if 配置.镜头反转:
            t*=-1
        self.glWidget.鼠标位移改变镜头(t.x,t.y)
        
    def 球动(self,x0,y0,x1,y1):
        d=配置.控制球大小
        p=self.控制球.mapFromParent(QPoint(x1,y1))
        if 0<=p.x()<=d and 0<=p.y()<=d:
            v=(vec(p.x(),p.y())-vec(d/2,d/2)).normalize()
            self.glWidget.控制=[-v.y,-v.x]
        if d/3<=p.x()<=d/3*2 and d/3<=p.y()<=d/3*2:
            net_client.udp_send(('跳',0,'开始施法'))

    def keyPressEvent(self, event):
        key=QKeyEvent(event).key()
        try:
            key = chr(key)
        except:
            None

        if key==16777216:   #ESC
            self.控制断开()
        if key=='W':
            self.glWidget.控制[0]+=1
        if key=='S':
            self.glWidget.控制[0]-=1
        if key=='A':
            self.glWidget.控制[1]+=1
        if key=='D':
            self.glWidget.控制[1]-=1
        if key==' ':
            net_client.udp_send(('跳',0,'开始施法'))
        if key=='Q':
            net_client.udp_send(('法术',3,'开始施法'))
        if key=='E':
            net_client.udp_send(('法术',4,'开始施法'))
        if key==16777248:   #SHIFT
            net_client.udp_send(('法术',5,'开始施法'))

    def keyReleaseEvent(self, event):
        key=QKeyEvent(event).key()
        try:
            key = chr(key)
        except:
            None
        if key=='W':
            self.glWidget.控制[0]-=1
        if key=='S':
            self.glWidget.控制[0]+=1
        if key=='A':
            self.glWidget.控制[1]-=1
        if key=='D':
            self.glWidget.控制[1]+=1
        if key=='Q':
            net_client.udp_send(('法术',3,'停止施法'))
        if key=='E':
            net_client.udp_send(('法术',4,'停止施法'))
        if key==16777248:   #SHIFT
            net_client.udp_send(('法术',5,'停止施法'))

    def 控制断开(self):
        self.setCursor(QCursor())
        self.glWidget.接管鼠标=False
        self.无控制遮罩.show()

    def 控制接上(self):
        self.setCursor(Qt.BlankCursor)
        self.glWidget.接管鼠标=True
        self.无控制遮罩.hide()

class GLWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        super(GLWidget, self).__init__(parent)
        self.resize(*配置.屏幕大小)
        self.世界钟=clock.clock()
        self.周期钟=clock.clock()
        self.绘图钟=clock.clock()
        self.接管鼠标 = True
        self.世界=env.主世界
        self.控制=[0,0]
        self.实际帧率=0
        self.绘图帧率=0
        self.逻辑帧率=0
        
    def initializeGL(self):
        glClearColor(0.4,0.6,1,0)
        # glClearColor(0.7,0.1,0.1,0)
        # glClearColor(0,0,0,0)
        glClearDepth(1.0)
        glEnable(GL_CULL_FACE)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_TEXTURE_2D)
        glPolygonMode(GL_FRONT, GL_FILL)

        import texture

        glGenBuffers(3000)

    def paintGL(self):
        # print(self.我.眼睛)


        if self.接管鼠标 and not 配置.surface模式:
            self.镜头修正()
            
        self.我.在走=False
        if any(self.控制):
            self.我.在走=True
            self.我.行走方向=self.向量取角(self.控制)
            
        if any(self.控制):
            net_client.udp_send(('走',True,self.向量取角(self.控制)))
        else:
            net_client.udp_send(('走',False,0))

        t1=self.周期钟.tick()
        self.绘图钟.tick()
        self.画面刷新()
        t2=self.绘图钟.tick()
        self.世界钟.tick()
        if True:
            try:
                self.世界.tp(t1)
            except:
                # 反正多线程错误多23333
                None
            for i in particle.particle_pool:
                    i.tp(t1)
        t3=self.世界钟.tick()

        t1+=1/10**6
        t2+=1/10**6
        t3+=1/10**6

        self.实际帧率+=1/t1*0.1
        self.绘图帧率+=1/t2*0.1
        self.逻辑帧率+=1/t3*0.1
        self.实际帧率*=10/11
        self.绘图帧率*=10/11
        self.逻辑帧率*=10/11
        self.parent().提示.setText('实际帧率: %d \n绘图帧率: %d \n逻辑帧率: %d\n' % (self.实际帧率, self.绘图帧率, self.逻辑帧率))

        self.update()

    @property
    def 我(self):
        try:
            return self.世界.单位池[env.my_id]
        except:
            return unit.人()

    def 向量取角(self,a):
        x,y=a[0],a[1]
        if x==0: 
            if y>0: return math.pi/2
            else: return -math.pi/2
        ans=math.atan(y/x)
        if x<0: ans+=math.pi
        return ans
        
    def 画面刷新(self):

        #3D
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_TEXTURE_2D)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) 
        
        glLoadIdentity()
        gluPerspective(配置.视角大小, 配置.屏幕大小[0]/配置.屏幕大小[1], 0.1, (配置.视距)*16)
        
        gluLookAt(*self.我.眼睛, *(self.我.眼睛+self.我.面向), 0,0,1)
        
        #预加载
        t=tuple(self.我.眼睛+ran_vec()*配置.预加载距离*random.random())
        env.主世界.预生成地形((int(t[0]),int(t[1])))
        
        self.绘图()

        #2D
        glDisable(GL_TEXTURE_2D)
        glLoadIdentity()
        
        with lines(color=(1,1,0.5),width=2):
            glVertex2f(配置.准星大小*配置.屏幕大小[1]/配置.屏幕大小[0],0)
            glVertex2f(-配置.准星大小*配置.屏幕大小[1]/配置.屏幕大小[0],0)
            glVertex2f(0,配置.准星大小)
            glVertex2f(0,-配置.准星大小)
    
    def 缓冲区域(self,m):
        块缓冲.添加(m)
        a=[]
        b=[]
        c=[]
        for i in self.世界.块索引[m]:
            块id=self.世界.全块[i]
            块=block.m[块id]
            x,y,z=i
            pos=numpy.array([x,y,z, x,y,z, x,y,z, x,y,z])
            if not (x,y,z+1) in self.世界.全块:
                t=块.画顶()
                a.append(numpy.array(t[1])+pos)
                b.append(numpy.array(t[0]))
                色=self.世界.亮度.get((x,y,z+1),15)
                c.append(numpy.ones(12)*(色+1)/16)
            if not (x,y,z-1) in self.世界.全块:
                t=块.画底()
                a.append(numpy.array(t[1])+pos)
                b.append(numpy.array(t[0]))
                色=self.世界.亮度.get((x,y,z-1),15)
                c.append(numpy.ones(12)*(色+1)/16)
            if not (x+1,y,z) in self.世界.全块:
                t=块.画左()
                a.append(numpy.array(t[1])+pos)
                b.append(numpy.array(t[0]))
                色=self.世界.亮度.get((x+1,y,z),15)
                c.append(numpy.ones(12)*(色+1)/16)
            if not (x-1,y,z) in self.世界.全块:
                t=块.画右()
                a.append(numpy.array(t[1])+pos)
                b.append(numpy.array(t[0]))
                色=self.世界.亮度.get((x-1,y,z),15)
                c.append(numpy.ones(12)*(色+1)/16)
            if not (x,y+1,z) in self.世界.全块:
                t=块.画前()
                a.append(numpy.array(t[1])+pos)
                b.append(numpy.array(t[0]))
                色=self.世界.亮度.get((x,y+1,z),15)
                c.append(numpy.ones(12)*(色+1)/16)
            if not (x,y-1,z) in self.世界.全块:
                t=块.画后()
                a.append(numpy.array(t[1])+pos)
                b.append(numpy.array(t[0]))
                色=self.世界.亮度.get((x,y-1,z),15)
                c.append(numpy.ones(12)*(色+1)/16)

        数据=块缓冲.数据字典[m]
        数据['顶点组']=numpy.float32(a).flatten()
        数据['纹理组']=numpy.float32(b).flatten()
        数据['颜色组']=numpy.float32(c).flatten()
        顶点数据数=数据['顶点组'].shape[0]
        顶点数=顶点数据数//3
        纹理数据数=数据['纹理组'].shape[0]
        glBindBuffer(GL_ARRAY_BUFFER, 数据['号']*3-2)
        glBufferData(GL_ARRAY_BUFFER, 顶点数据数*4,  数据['顶点组'], GL_STATIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, 数据['号']*3-1)
        glBufferData(GL_ARRAY_BUFFER, 纹理数据数*4,  数据['纹理组'], GL_STATIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, 数据['号']*3)
        glBufferData(GL_ARRAY_BUFFER, 顶点数据数*4,  数据['颜色组'], GL_STATIC_DRAW)

    def 绘制区域(self,m):
        # 减支
        # 其实反而会变慢23333
        # v=vec(m[0]*16,m[1]*16,m[2]*16)
        # 目至各顶点=(i-self.我.眼睛 for i in v.角枚举(vec(16,16,16)))
        # if not any(i.同侧(self.我.面向) for i in 目至各顶点):
        #     return

        if m not in 块缓冲.数据字典:
            if random.random()>0.03:    # 首次加载分步缓冲，其实应该改线程的2333
                return
            self.缓冲区域(m)
        elif not 块缓冲.数据字典[m]['可用']:
            self.缓冲区域(m)


        数据=块缓冲.数据字典[m]
        数据数=数据['顶点组'].shape[0]
        顶点数=数据数//3
        
        glBindBuffer(GL_ARRAY_BUFFER, 数据['号']*3-2);
        glVertexPointer(3, GL_FLOAT, 0, None);
        glBindBuffer(GL_ARRAY_BUFFER, 数据['号']*3-1);
        glTexCoordPointer(2, GL_FLOAT, 0, None)
        glBindBuffer(GL_ARRAY_BUFFER, 数据['号']*3);
        glColorPointer(3, GL_FLOAT, 0, None)

        glDrawArrays(GL_QUADS, 0, 顶点数);
        

    def 绘图(self):
        # 画天空盒子
        # x,y,z=self.我.眼睛
        # x-=50;y-=50;z-=50
        # glTranslatef(x,y,z)
        # gl_list.画gl_list('天空盒子')
        # glTranslatef(-x,-y,-z)
        
        # 画地形
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_TEXTURE_COORD_ARRAY)
        glEnableClientState(GL_COLOR_ARRAY)
        glBindTexture(GL_TEXTURE_2D, env.m['全纹理'])
        my_x,my_y,my_z=self.我.位置.intize
        for dx in range(-配置.视距,配置.视距+1):
            for dy in range(-配置.视距,配置.视距+1):
                for dz in range(-配置.视距,配置.视距+1):
                    m=my_x//16+dx, my_y//16+dy, my_z//16+dz
                    if m not in self.世界.块索引: 
                        continue
                    self.绘制区域(m)
        glBindBuffer(GL_ARRAY_BUFFER, 0);
            
        # 画粒子效果
        glDisable(GL_CULL_FACE)
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        for i in particle.particle_pool:
            i.draw()
        glPolygonMode(GL_FRONT, GL_FILL)
        glEnable(GL_CULL_FACE)


        # 画单位
        glColor(1,1,1)
        t=copy.copy(self.世界.单位池)
        for i in t:
            i=t[i]
            if i.id==self.我.id:
                continue
            with temp_translate(*i.位置):
                i.draw()

        t=self.我.所面向的块      
        if t:
            x,y,z=t
            glColor(0.8,0.8,0.8)
            d=0.005
            line_box(x-d,y-d,z-d,1+2*d,1+2*d,1+2*d)
            
    def 镜头修正(self):
        鼠标位置=self.mapFromGlobal(QCursor.pos())
        x,y=鼠标位置.x()-配置.屏幕大小[0]//2,鼠标位置.y()-配置.屏幕大小[1]//2
        
        self.鼠标位移改变镜头(x,y)

        QCursor.setPos(self.mapToGlobal(QPoint(配置.屏幕大小[0]//2,配置.屏幕大小[1]//2)))

    def 鼠标位移改变镜头(self,x,y):
        if x!=0 or y!=0:
            if not 配置.surface模式:
                x*=配置.鼠标速度
                y*=配置.鼠标速度
            else:
                x*=配置.卷动速度
                y*=配置.卷动速度
            self.我.面角[0]-=x
            self.我.面角[1]-=y
            self.我.面角[1]=limit(self.我.面角[1],-pi/2+0.1,pi/2-0.1)
            net_client.udp_send(('面角',self.我.面角[0],self.我.面角[1]))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = 主窗口()
    app.installEventFilter(window)
    if 配置.全屏:
        window.showFullScreen()
    else:
        window.show()
    sys.exit(app.exec_())