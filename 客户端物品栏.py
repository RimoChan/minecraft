import sys
import PyQt5
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import env

import net_client

class 阴影文字(QLabel):
    def __init__(self,size,*d):
        super().__init__(*d)
        self.resize(*size)
        self.底=QLabel(self)
        self.底.resize(*size)
        self.底.move(1,1)
        self.自身=QLabel(self)
        self.自身.resize(*size)
        self.自身.setStyleSheet("color:#fff;")
    def setText(self,s):
        self.底.setText(s)
        self.自身.setText(s)

class 物品(QWidget):
    def __init__(self,序号,*l):
        super().__init__(*l)
        self.resize(50,50)
        self.序号=序号
        self.图=QLabel(self)
        self.图.resize(50,50)
        self.图.setScaledContents(True)
        self.字=阴影文字((50,50),self)
        self.字.setStyleSheet("font-size:18px;font-family:consolas;")
        self.字.resize(50,50)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton: 
            net_client.udp_send(('选择物品',self.序号))

class 物品栏(QWidget):
    def __init__(self,*l):
        super().__init__(*l)
        self.resize(600,400)
        self.setWindowTitle("物品栏")
        self.空间=[物品(i,self) for i in range(12*8)]
        self.setWindowFlags(Qt.FramelessWindowHint|Qt.WindowStaysOnTopHint)
        for i,l in enumerate(self.空间):
            l.move(i%12*50,i//12*50)

    def 刷新(self,info):
        if not info: return
        for i in range(12*8):
            self.空间[i].图.setText(' ')
            self.空间[i].字.setText(' ')
        for i,x in enumerate(info):
            self.空间[i].图.setPixmap(QPixmap('装备图/'+x[0]))
            self.空间[i].字.setText(str(x[1]))

    def keyPressEvent(self, event):
        key=QKeyEvent(event).key()
        if key==16777216 :   #ESC
            env.主窗口.控制接上()

if __name__=='__main__':
    app = QApplication(sys.argv)
    window = 物品栏()
    window.刷新([('eaglesong.jpg',32)])
    window.show()
    sys.exit(app.exec_())