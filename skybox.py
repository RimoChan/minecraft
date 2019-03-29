from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import gl_list
import env

纹理 = ['box_1_up', 'box_2_ft', 'box_3_bk', 'box_4_lf', 'box_5_rt', 'box_6_dn']

顶, 前, 后, 左, 右, 底 = [env.m[i] for i in 纹理]

with gl_list.做gl_list('天空盒子'):
    glBindTexture(GL_TEXTURE_2D, 顶)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex3f(120, 0, 120)
    glTexCoord2f(0, 1)
    glVertex3f(0, 0, 120)
    glTexCoord2f(1, 1)
    glVertex3f(0, 120, 120)
    glTexCoord2f(1, 0)
    glVertex3f(120, 120, 120)
    glEnd()

    glBindTexture(GL_TEXTURE_2D, 底)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 1)
    glVertex3f(120, 0, 0)
    glTexCoord2f(1, 1)
    glVertex3f(120, 120, 0)
    glTexCoord2f(1, 0)
    glVertex3f(0, 120, 0)
    glTexCoord2f(0, 0)
    glVertex3f(0, 0, 0)
    glEnd()

    glBindTexture(GL_TEXTURE_2D, 前)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex3f(120, 120, 0)
    glTexCoord2f(0, 1)
    glVertex3f(120, 120, 120)
    glTexCoord2f(1, 1)
    glVertex3f(0, 120, 120)
    glTexCoord2f(1, 0)
    glVertex3f(0, 120, 0)
    glEnd()

    glBindTexture(GL_TEXTURE_2D, 后)
    glBegin(GL_QUADS)
    glTexCoord2f(1, 0)
    glVertex3f(120, 0, 0)
    glTexCoord2f(0, 0)
    glVertex3f(0, 0, 0)
    glTexCoord2f(0, 1)
    glVertex3f(0, 0, 120)
    glTexCoord2f(1, 1)
    glVertex3f(120, 0, 120)
    glEnd()

    glBindTexture(GL_TEXTURE_2D, 右)
    glBegin(GL_QUADS)
    glTexCoord2f(1, 0)
    glVertex3f(120, 120, 0)
    glTexCoord2f(0, 0)
    glVertex3f(120, 0, 0)
    glTexCoord2f(0, 1)
    glVertex3f(120, 0, 120)
    glTexCoord2f(1, 1)
    glVertex3f(120, 120, 120)
    glEnd()

    glBindTexture(GL_TEXTURE_2D, 左)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex3f(0, 120, 0)
    glTexCoord2f(0, 1)
    glVertex3f(0, 120, 120)
    glTexCoord2f(1, 1)
    glVertex3f(0, 0, 120)
    glTexCoord2f(1, 0)
    glVertex3f(0, 0, 0)
    glEnd()
