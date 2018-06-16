import contextlib
import functools

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from PIL import Image
import os
import numpy as np

@contextlib.contextmanager
def temp_translate(x,y,z):
    glTranslatef(x,y,z)
    yield
    glTranslatef(-x,-y,-z)

@contextlib.contextmanager
def temp_scale(x,y,z):
    glScalef(x,y,z)
    yield
    glScalef(1/x,1/y,1/z)

m={'x':(1,0,0),'y':(0,1,0),'z':(0,0,1)}
@contextlib.contextmanager
def temp_rotate(d,c):
    glRotatef(d,*m[c])
    yield
    glRotatef(-d,*m[c])

def vec_rotate(a,b):
    a/=np.linalg.norm(a)
    b/=np.linalg.norm(b)
    v=np.cross(a,b)
    d=np.degrees(np.arccos(np.dot(a,b)))
    glRotatef(d,*v)

@contextlib.contextmanager
def temp_vec_rotate(a,b):
    vec_rotate(a,b)
    yield
    vec_rotate(b,a)

@contextlib.contextmanager
def new_list(list_id):
    glNewList(list_id,GL_COMPILE)
    yield
    glEndList()

@contextlib.contextmanager
def lines(color=None,width=None):
    if color:
        glColor3f(*color)
    if width:
        glLineWidth(width)
    glBegin(GL_LINES)
    yield
    glEnd() 

@contextlib.contextmanager
def points(size=None,color=None):
    if color:
        glColor3f(*color)
    if size:
        glPointSize(size)
    glBegin(GL_POINTS)
    yield
    glEnd() 

@contextlib.contextmanager
def quads(texture=None):
    if texture:
        glBindTexture(GL_TEXTURE_2D, texture)
    glBegin(GL_QUADS)
    yield
    glEnd()
    

def line_box(x0,y0,z0,x,y,z):
    glBindTexture(GL_TEXTURE_2D, 0)
    glPolygonMode(GL_FRONT_AND_BACK ,GL_LINE)
    glDisable(GL_CULL_FACE)
    with temp_translate(x0,y0,z0):
        with quads():   
            glVertex3f(0, y, 0)
            glVertex3f(0, y, z)
            glVertex3f(x, y, z)
            glVertex3f(x, y, 0)
        
        with quads():   
            glVertex3f(0, 0, 0)
            glVertex3f(x, 0, 0)
            glVertex3f(x, 0, z)
            glVertex3f(0, 0, z)
        
        with quads():     
            glVertex3f(x, 0, 0)
            glVertex3f(x, y, 0)
            glVertex3f(x, y, z) 
            glVertex3f(x, 0, z)
        
        with quads():   
            glVertex3f(0, 0, 0)
            glVertex3f(0, 0, z)
            glVertex3f(0, y, z)
            glVertex3f(0, y, 0)
    
    glEnable(GL_CULL_FACE)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)