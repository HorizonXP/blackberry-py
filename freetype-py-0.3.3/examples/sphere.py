#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import math
import numpy
import OpenGL.GL as gl
import OpenGL.GLU as glu
import OpenGL.GLUT as glut
from freetype import *

base, texid = 0, 0
dx = 0
dy = 0
text  = 'Hello World !'
angles = numpy.random.randint(0,360,20).astype(float)
radius = numpy.sort(numpy.random.uniform(1,2,20))


def makefont(filename, size):
    global texid, dx, dy

    # Load font  and check it is monotype
    face = Face(filename)
    face.set_char_size( size*64 )
    if not face.is_fixed_width:
        raise 'Font is not monotype'

    # Determine largest glyph size
    width, height, ascender, descender = 0, 0, 0, 0
    for c in range(32,128):
        face.load_char( chr(c), FT_LOAD_RENDER | FT_LOAD_FORCE_AUTOHINT )
        bitmap    = face.glyph.bitmap
        width     = max( width, bitmap.width )
        ascender  = max( ascender, face.glyph.bitmap_top )
        descender = max( descender, bitmap.rows-face.glyph.bitmap_top )
    height = ascender+descender

    # Generate texture data
    Z = numpy.zeros((height*6, width*16), dtype=numpy.ubyte)
    for j in range(6):
        for i in range(16):
            face.load_char(chr(32+j*16+i), FT_LOAD_RENDER | FT_LOAD_FORCE_AUTOHINT )
            bitmap = face.glyph.bitmap
            x = i*width  + face.glyph.bitmap_left
            y = j*height + ascender - face.glyph.bitmap_top
            Z[y:y+bitmap.rows,x:x+bitmap.width].flat = bitmap.buffer

    # Bound texture
    texid = gl.glGenTextures(1)
    gl.glBindTexture( gl.GL_TEXTURE_2D, texid )
    gl.glTexParameterf( gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR )
    gl.glTexParameterf( gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR )
    gl.glTexImage2D( gl.GL_TEXTURE_2D, 0, gl.GL_ALPHA, Z.shape[1], Z.shape[0], 0,
                     gl.GL_ALPHA, gl.GL_UNSIGNED_BYTE, Z )
    dx, dy = width/float(Z.shape[1]), height/float(Z.shape[0])



def spheric(r, theta, phi):
    theta = theta/180.0 * math.pi
    phi = phi/180.0 * math.pi
    return (r*math.sin(theta)*math.cos(phi),
            r*math.sin(theta)*math.sin(phi),
            r*math.cos(theta))


def on_display():
    global Theta, Phi, dx, dy, angles
    gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
    gl.glColor(0,0,0,1)

    gl.glPushMatrix()
    gl.glBindTexture( gl.GL_TEXTURE_2D, texid )
    gl.glRotatef(90, 1,0,0)
    gl.glRotatef(Theta, 0,0,1)
#    gl.glRotatef(Phi, 0,1,0)

    gl.glColor(1,1,1,1)
    gl.glEnable(gl.GL_BLEND)
    gl.glBlendFunc (gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

    phi = 0
    theta = 85
    for k in range(len(angles)):
        r = radius[k]
        angle = angles[k]
        gl.glRotatef(angle, 0,1,1)
        #gl.glColor(r-1,r-1,r-1,1)
        #r = 1.5
        for c in text:
            i = ord(c)
            x,y = i%16, i//16-2
            gl.glBegin( gl.GL_QUADS )
            x0,y0,z0 = spheric(r, theta, phi)
            x1,y1,z1 = spheric(r+1, theta, phi)
            gl.glNormal3f(x1-x0,y1-y0,z1-z0)
            gl.glTexCoord2f( (x  )*dx, (y+1)*dy ),  gl.glVertex(spheric(r, theta,   phi+5))
            gl.glTexCoord2f( (x  )*dx, (y  )*dy ),  gl.glVertex(spheric(r, theta+10, phi+5))
            gl.glTexCoord2f( (x+1)*dx, (y  )*dy ),  gl.glVertex(spheric(r, theta+10, phi-5))
            gl.glTexCoord2f( (x+1)*dx, (y+1)*dy ),  gl.glVertex(spheric(r, theta,   phi-5))
            gl.glEnd()
            phi = phi - 10
            
    angles += numpy.random.random(20)*.1
           
    gl.glPopMatrix()
    glut.glutSwapBuffers()


def on_reshape(width, height):
    gl.glViewport(0, 0, width, height)
    gl.glMatrixMode( gl.GL_PROJECTION )
    gl.glLoadIdentity( )
    glu.gluPerspective( 45.0, float(width)/float(height), 2.0, 10.0 )
    gl.glMatrixMode( gl.GL_MODELVIEW )
    gl.glLoadIdentity( )
    gl.glTranslatef( 0.0, 0.0, -5.0 )


def on_keyboard(key, x, y):
    if key == '\033':
        sys.exit()

def on_timer(value):
    global Theta
    Theta += 0.5
    glut.glutPostRedisplay()
    glut.glutTimerFunc(10, on_timer, 0)


if __name__ == '__main__':
    glut.glutInit(sys.argv)
    glut.glutInitDisplayMode(glut.GLUT_DOUBLE | glut.GLUT_RGB | glut.GLUT_DEPTH)
    glut.glutCreateWindow("Text on spheres")
    glut.glutReshapeWindow(800, 800)
    glut.glutDisplayFunc(on_display)
    glut.glutReshapeFunc(on_reshape)
    glut.glutKeyboardFunc(on_keyboard)
    glut.glutTimerFunc(10, on_timer, 0)
    gl.glClearColor(0,0,0,1);
    Theta, Phi = 90, 0
    gl.glTexEnvf( gl.GL_TEXTURE_ENV, gl.GL_TEXTURE_ENV_MODE, gl.GL_MODULATE )
    gl.glEnable( gl.GL_DEPTH_TEST )
    gl.glEnable( gl.GL_BLEND )
    gl.glEnable( gl.GL_COLOR_MATERIAL )
    gl.glColorMaterial( gl.GL_FRONT_AND_BACK, gl.GL_AMBIENT_AND_DIFFUSE )
    gl.glBlendFunc( gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA )
    gl.glEnable( gl.GL_TEXTURE_2D )

    gl.glLightfv (gl.GL_LIGHT0, gl.GL_DIFFUSE, (1.0, 0.0, 0.0, 1.0))
    gl.glLightfv (gl.GL_LIGHT0, gl.GL_AMBIENT, (0.3, 0.0, 0.0, 1.0))
    gl.glLightfv (gl.GL_LIGHT0, gl.GL_SPECULAR,(0.0, 0.0, 0.0, 0.0))
    gl.glLightfv (gl.GL_LIGHT0, gl.GL_POSITION,(2.0, 2.0, 2.0, 0.0))

    gl.glLightfv (gl.GL_LIGHT1, gl.GL_DIFFUSE, (0.0, 1.0, 1.0, 1.0))
    gl.glLightfv (gl.GL_LIGHT1, gl.GL_AMBIENT, (0.0, 0.1, 0.3, 1.0))
    gl.glLightfv (gl.GL_LIGHT1, gl.GL_SPECULAR,(0.0, 0.0, 0.0, 0.0))
    gl.glLightfv (gl.GL_LIGHT1, gl.GL_POSITION,(-2.0, 2.0, 2.0, 0.0))

    gl.glEnable (gl.GL_LIGHT0)
    gl.glEnable (gl.GL_LIGHT1)
    gl.glEnable (gl.GL_LIGHTING)
    makefont( './VeraMono.ttf', 64 )
    glut.glutMainLoop()

