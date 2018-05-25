import socket
import threading
import pickle
import time
import zlib
import random

from 配置 import 配置
import clock
import env
import block

myclock=clock.clock()

def all_send(self,data):
    data=zlib.compress(pickle.dumps(data))
    self.sendto(data, tuple(配置.服务器地址))
socket.socket.all_send=all_send

udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
def udp_send(data):
    udp_socket.all_send(data)

def recv():
    udp_send('gogogo!')
    包大小=10000
    while True:
        try:
            all_data,addr = udp_socket.recvfrom(包大小)
            包大小=int((包大小*19+len(all_data)*1.6+800)/20)
        except Exception as e:
            if e.errno==10040:
                print('包大小:%d，溢出。' %包大小)
                包大小*=2
                包大小+=2048
                continue
            raise e

        all_data=zlib.decompress(all_data)
        all_data=pickle.loads(all_data)
        
        无效=False
        for key,value in all_data.items():
            if key=='id':
                env.my_id=value
            if key=='单位':
                env.主世界.单位池=value
            if key=='块':
                t='块'
                print()
                print('数据起始:',value[0][0])
                print('已有长度:',len(env.主世界.记录))
                if len(value)>80:
                    env.启用粒子=False
                if value[0][0]==len(env.主世界.记录):
                    for i in value:
                        env.主世界.记录.append(i[1])
                        if i[1][0]=='放':
                            i=i[1]
                            x,y,z,id=i[1],i[2],i[3],i[4]
                            env.主世界.放块(x,y,z,block.m[id],True)
                        elif i[1][0]=='去':
                            i=i[1]
                            x,y,z=i[1],i[2],i[3]
                            env.主世界.去块(x,y,z,True)
                if len(value)>80:
                    env.启用粒子=True
                无效=True
        if not 无效:
            udp_send(('块',len(env.主世界.记录)))
            
# def exchange():
    # udp_send('gogogo!')
    # while True:
        # time.sleep(0.02)
        # udp_send(('块',len(env.主世界.记录)))
        
def close():
    udp_socket.close()
    print('socket关闭')

t = threading.Thread(target=recv)
t.setDaemon(True)
t.start()
# t = threading.Thread(target=exchange)
# t.setDaemon(True)
# t.start()


if __name__=='__main__':
    env.客户端=True
    import world
    env.主世界=world.世界()
    time.sleep(10)