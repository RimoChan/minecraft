from vec import *
import env
import particle


def 爆炸(v):
    x, y, z = v
    for i in range(150):
        particle.particle(14, x, y, z, speed=5, t=rd(0.3, 1.3), size=0.3, 重力系数=0.15)
    for i in env.主世界.单位池:
        u = env.主世界.单位池[i]
        if (v - u.位置).mo < 4:
            u.基础速度 -= (v - u.位置).normalize() * 8
            u.基础速度.z += 4
        x, y, z = v.intize
        for dx in range(-3, 4):
            for dy in range(-3, 4):
                for dz in range(-3, 4):
                    if (vec(x + dx, y + dy, z + dz) - v).mo < 3:
                        env.主世界.去块(x + dx, y + dy, z + dz)
