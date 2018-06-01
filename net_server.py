import socket,time
import threading
import pickle
import random
import zlib
import copy

import unit
import clock
import env

from tool import *

收包钟=clock.clock()
收包间隔=0
udp钟=clock.clock()

address=('0.0.0.0',23333)
address2=('0.0.0.0',23334)

udp池=dict()
包计数=0

def serv_all_send(self,data,addr):
    b_data=pickle.dumps(data)
    b_data=zlib.compress(b_data)
    self.sendto(b_data, addr)
    if random.random()<1/150:
        print(': 抽样到发送了大小为%.1fKB的数据。'% (len(b_data)/1000.0) )
socket.socket.serv_all_send=serv_all_send
    
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.bind(address)
udp_socket2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket2.bind(address2)

def udp处理():
    while True:
        mir=copy.copy(udp池)
        t=udp钟.tick()
        for addr in mir:
            u=mir[addr]
            udp_socket2.serv_all_send({'id':u['id'],'单位':env.发送单位},
                    addr)
            u['time']-=t
            if u['time']<0:
                try:
                    env.主世界.单位池[u['id']].die()
                except:
                    None
                print('从',addr,'的udp连线断开了')
                udp池.pop(addr)
        time.sleep(0.03)
    
        
def server():
    def udp_listen(udp_socket):
        while True:
            data, addr = udp_socket.recvfrom(2000)
      
            a=收包钟.tick()+0.0001
            global 收包间隔
            收包间隔=(收包间隔*30+a)/31
            if random.random()<0.001:
                print('收包帧率:',1/收包间隔)
            
            if addr not in udp池:
                print('UDP从',addr,'连进来了。')
                他=unit.人()
                env.主世界.单位池.加(他)
                udp池[addr]={'time':3,'id':他.id}
            else:
                udp池[addr]['time']=3
                
            #处理信息
            data=pickle.loads(zlib.decompress(data))
            if isinstance(data,tuple):
                try:
                    我=env.主世界.单位池[udp池[addr]['id']]
                    # print(data)
                    if data[0]=='法术':
                        if data[2]=='开始施法':
                            我.法术[data[1]].call()
                        if data[2]=='停止施法':
                            我.法术[data[1]].stop()
                            
                    if data[0]=='走':
                        我.在走=data[1]
                        我.行走方向=data[2]
                    if data[0]=='跳':
                        我.跳()
                    if data[0]=='面角':
                        我.面角[0]=data[1]
                        我.面角[1]=data[2]
                        # 我.面角[1]=limit(我.面角[1],-pi/2+0.1,pi/2-0.1)
                    if data[0]=='块':
                        if data[1]<len(env.主世界.记录):
                            q=[]
                            i=data[1]
                            for r in env.主世界.记录[data[1]:data[1]+2000]:
                                q.append((i,r))
                                i+=1
                            udp_socket2.serv_all_send({'块':q},
                            addr)
                            print('收到:',data[1],'发至:',i)
                except Exception as e:
                    print(e)
            elif isinstance(data,str):
                pass
            else:
                print(data)
                
    t0 = threading.Thread(target=lambda:udp_listen(udp_socket))
    t0.setDaemon(True)
    t0.start()
    
    t1 = threading.Thread(target=udp处理)
    t1.setDaemon(True)
    t1.start()
    
print('监听启动了。')
t = threading.Thread(target=server)
t.setDaemon(True)
t.start()