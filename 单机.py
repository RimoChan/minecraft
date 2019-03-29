import multiprocessing

def 服务():
    import 服务主机
    服务主机.服务()

if __name__=='__main__':
    p = multiprocessing.Process(target = 服务)
    p.start()
    
    import 客户端
    客户端.开始玩()