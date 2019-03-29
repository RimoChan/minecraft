import numpy

# 每個字典項 : {可用性，顶点组，纹理组}
缓冲数 = 0
数据字典 = {}


def 添加(m):
    if m in 数据字典:
        数据字典[m]['可用'] = True
        数据字典[m]['顶点组'] = numpy.zeros(shape=[80000], dtype=numpy.float32)
        数据字典[m]['纹理组'] = numpy.zeros(shape=[60000], dtype=numpy.float32)
        数据字典[m]['颜色组'] = numpy.zeros(shape=[80000], dtype=numpy.float32)
    else:
        global 缓冲数
        缓冲数 += 1
        数据字典[m] = {
            '可用': True,
            '顶点组': numpy.zeros(shape=[80000], dtype=numpy.   float32),
            '纹理组': numpy.zeros(shape=[60000], dtype=numpy.   float32),
            '颜色组': numpy.zeros(shape=[80000], dtype=numpy.   float32),
            '号': 缓冲数
        }
