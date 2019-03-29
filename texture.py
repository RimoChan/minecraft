from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PIL import Image
import os

import env

glGenTextures(150)

env.m = dict()

id = 0
for 名字 in os.listdir('texture/'):
    if not 名字.endswith('png'):
        continue
    id += 1

    img = Image.open('texture/' + 名字)
    width, height = img.size
    img = img.tobytes('raw', 'RGBA', 0, -1)

    env.m[名字.split('.')[0]] = id
    glBindTexture(GL_TEXTURE_2D, id)
    glTexImage2D(GL_TEXTURE_2D, 0, 4,
                 width, height, 0, GL_RGBA,
                 GL_UNSIGNED_BYTE, img)
    glTexParameterf(GL_TEXTURE_2D,
                    GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D,
                    GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    # glTexEnvf(GL_TEXTURE_ENV,GL_TEXTURE_ENV_MODE, GL_REPLACE)
