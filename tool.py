import math
import random
pi = math.pi


def intt(x):
    if x > 0:
        return int(x)
    return int(x + 999) - 999


def limit(a, q, w):
    if q > w:
        q, w = w, q
    if a < q:
        return q
    if a > w:
        return w
    return a


def rd(a, b):
    if all([isinstance(x, int)for x in (a, b)]):
        return random.randint(a, b)
    else:
        return random.random() * (b - a) + a


def de(li, f):
    删掉的 = []
    for i in range(len(li))[::-1]:
        if f(li[i]):
            删掉的.append(li[i])
            li.pop(i)
    return 删掉的


class h_list(list):
    def __init__(self, owner):
        super().__init__()
        self.owner = owner

    def append(self, x):
        x.owner = self.owner
        list.append(self, x)

    def __str__(self):
        return list.__str__(self)


a = []
all_t = 0


def time_log(t, server_mode=False):
    global all_t
    all_t += t
    if len(a) < 100:
        a.append(t)
    else:
        a[rd(0, 99)] = t
    if all_t > 3:
        all_t -= 3
        n = (1 / (sum(a) / len(a)))
        print('平均更新次数/s: %d，' % n, '最慢更新用时: %.3f。' % max(a))
        if server_mode and n < 80:
            print('------------------------------')
            print('-----------性能警告-----------')
            print('在过去的1秒内只更新了%d次，' % n, '最慢更新用时: %.3f。' % max(a))
            print('也许你的服务器不适合支持这个规模的游戏……')
            print('------------------------------')
