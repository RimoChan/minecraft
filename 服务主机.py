import threading
import time
import random
import math
import copy
from math import sin,cos
from tool import *

import clock
import env
import world

clock=clock.clock()
env.主世界=world.世界()
世界=env.主世界
print('主循环启动了。')

import net_server
import atexit
print('按ctrl-c来安全退出。')

atexit.register(env.主世界.保存)

try:
    运行时间=0
    while True:
        time_passed = clock.tick()
        if time_passed<0.01:   #限制性能
            clock.back()
            time.sleep(0.01)
            time_passed=clock.tick()
        if time_passed>0.02:
            time_passed=0.02 #保证刷新均匀
        运行时间+=time_passed
        env.主世界.tp(time_passed)
        env.发送单位=env.主世界.单位池
except Exception as e:
    env.主世界.保存()


        
     
    
