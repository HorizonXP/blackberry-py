'''The code in this file was ported to Python and Pyggles from
the original JavaScript and WebGL code by emeric florence
at http://github.com/boblemarin/FLU and is covered under the
Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License.
See http://creativecommons.org/licenses/by-nc-sa/3.0/
'''


import os
import array
import math
from random import random

from bb.gles import *
from pyggles import shaders, drawable
from pyggles.rect import Rect
from pyggles.drawing import context, Drawing
from pyggles.timer import Timer


FOLDER = os.path.dirname(__file__)


class OglDemo(drawable.Drawable):
    NUM_LINES = 5000

    def init(self):
        '''Prepare for eventual drawing.
        Called from the rendering thread.'''
        print("setup()")
        vs = shaders.Shader(os.path.join(FOLDER, 'shader1.vert'))
        fs = shaders.Shader(os.path.join(FOLDER, 'shader1.frag'))
        self.prog = shaders.Program(vs, fs)
        self.prog.dump()

        self.touched = False
        sw, sh = self.drawing.size
        self.tw = sw / 2
        self.th = sh / 2
        self.tratio = sw / sh

        self.start_timer()


    def start_timer(self):
        def request_redraw(timer):
            self.drawing.redraw = True
        Timer(period=1/60, oneshot=False, callback=request_redraw).start()


    def onTouch(self, action, x, y):
        if action in {0, 1}:
            self.touchX = (x / self.tw - 1) * self.tratio
            self.touchY = -(y / self.th - 1)
            self.touched = True
        else:
            self.touched = False


    def resize(self):
        '''Initialises WebGL and creates the 3D scene.'''
        #    Set the viewport to the drawing width and height
        cw, ch = self.drawing.size
        glViewport(0, 0, cw, ch)

        print('resize()')

        #    Install the program as part of the current rendering state
        self.prog.use()

        #    Get the vertexPosition attribute from the linked shader program
        self.vertexPosition = self.prog.attribute('vertexPosition')

        #    Enable the vertexPosition vertex attribute array. If enabled, the array
        #    will be accessed an used for rendering when calls are made to commands like
        #    gl.drawArrays, gl.drawElements, etc.
        glEnableVertexAttribArray(self.vertexPosition)

        #    Clear the color buffer (r, g, b, a) with the specified color
        glClearColor(0.0, 0.0, 0.0, 1.0)

        #    Clear the depth buffer. The value specified is clamped to the range [0,1].
        #    More info about depth buffers: http://en.wikipedia.org/wiki/Depth_buffer
        glClearDepthf(1.0)

        #    Enable depth testing. This is a technique used for hidden surface removal.
        #    It assigns a value (z) to each pixel that represents the distance from this
        #    pixel to the viewer. When another pixel is drawn at the same location the z
        #    values are compared in order to determine which pixel should be drawn.
        # gl.enable(gl.DEPTH_TEST);

        glEnable(GL_BLEND)
        glDisable(GL_DEPTH_TEST)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE)

        #    Specify which function to use for depth buffer comparisons. It compares the
        #    value of the incoming pixel against the one stored in the depth buffer.
        #    Possible values are (from the OpenGL documentation):
        #    GL_NEVER - Never passes.
        #    GL_LESS - Passes if the incoming depth value is less than the stored depth value.
        #    GL_EQUAL - Passes if the incoming depth value is equal to the stored depth value.
        #    GL_LEQUAL - Passes if the incoming depth value is less than or equal to the stored depth value.
        #    GL_GREATER - Passes if the incoming depth value is greater than the stored depth value.
        #    GL_NOTEQUAL - Passes if the incoming depth value is not equal to the stored depth value.
        #    GL_GEQUAL - Passes if the incoming depth value is greater than or equal to the stored depth value.
        #    GL_ALWAYS - Always passes.
        # gl.depthFunc(gl.LEQUAL);

        #    Now create a shape.
        #    First create a vertex buffer in which we can store our data.
        self.vertexBuffer = GLuint()
        glGenBuffers(1, byref(self.vertexBuffer))

        #    Bind the buffer object to the ARRAY_BUFFER target.
        glBindBuffer(GL_ARRAY_BUFFER, self.vertexBuffer)

        #    Specify the vertex positions (x, y, z)
        self.vertices = array.array('f')
        self.ratio = cw / ch
        self.velocities = array.array('f')
        for i in range(self.NUM_LINES):
            self.vertices.extend([0, 0, 1.83])
            # (random() * 2 - 1)*ratio, random() * 2 - 1, 1.83 )
            self.velocities.extend([(random() * 2 - 1)*.05,
                (random() * 2 - 1)*.05,
                .93 + random()*.02])

        # self.vertices = self.make_vector(self.vertices)

        #    Creates a new data store for the vertices array which is bound to the ARRAY_BUFFER.
        #    The third paramater indicates the usage pattern of the data store. Possible values are
        #    (from the OpenGL documentation):
        #    The frequency of access may be one of these:
        #    STREAM - The data store contents will be modified once and used at most a few times.
        #    STATIC - The data store contents will be modified once and used many times.
        #    DYNAMIC - The data store contents will be modified repeatedly and used many times.
        #    The nature of access may be one of these:
        #    DRAW - The data store contents are modified by the application, and used as the source for
        #           GL drawing and image specification commands.
        #    READ - The data store contents are modified by reading data from the GL, and used to return
        #           that data when queried by the application.
        #    COPY - The data store contents are modified by reading data from the GL, and used as the source
        #           for GL drawing and image specification commands.
        addr, size = self.vertices.buffer_info()
        # glBufferData(GL_ARRAY_BUFFER, sizeof(self.vertices), self.vertices, GL_DYNAMIC_DRAW)
        glBufferData(GL_ARRAY_BUFFER, size * self.vertices.itemsize, addr, GL_DYNAMIC_DRAW)

        #    Clear the color buffer and the depth buffer
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        #    Define the viewing frustum parameters
        #    More info: http://en.wikipedia.org/wiki/Viewing_frustum
        #    More info: http://knol.google.com/k/view-frustum
        fieldOfView = 30.0
        aspectRatio = cw / ch
        nearPlane = 1.0
        farPlane = 10000.0
        top = nearPlane * math.tan(fieldOfView * math.pi / 360.0)
        bottom = -top
        right = top * aspectRatio
        left = -right

        #     Create the perspective matrix. The OpenGL function that's normally used for this,
        #     glFrustum() is not included in the WebGL API. That's why we have to do it manually here.
        #     More info: http://www.cs.utk.edu/~vose/c-stuff/opengl/glFrustum.html
        a = (right + left) / (right - left)
        b = (top + bottom) / (top - bottom)
        c = (farPlane + nearPlane) / (farPlane - nearPlane)
        d = (2 * farPlane * nearPlane) / (farPlane - nearPlane)
        x = (2 * nearPlane) / (right - left)
        y = (2 * nearPlane) / (top - bottom)
        perspectiveMatrix = self.make_vector([
            x, 0, a, 0,
            0, y, b, 0,
            0, 0, c, d,
            0, 0, -1, 0
            ])

        #     Create the modelview matrix
        #     More info about the modelview matrix: http://3dengine.org/Modelview_matrix
        #     More info about the identity matrix: http://en.wikipedia.org/wiki/Identity_matrix
        modelViewMatrix = self.make_vector([
            1, 0, 0, 0,
            0, 1, 0, 0,
            0, 0, 1, 0,
            0, 0, 0, 1
            ])

        #     Get the vertex position attribute location from the shader program
        vertexPosAttribLocation = self.prog.attribute('vertexPosition')
        #     colorLoc = gl.getVaryingLocation(gl.program, "vColor");
        #     alert("color loc : " + colorLoc );
        #     Specify the location and format of the vertex position attribute
        glVertexAttribPointer(vertexPosAttribLocation, 3, GL_FLOAT, GL_FALSE, 0, 0)
        # gl.vertexAttribPointer(colorLoc, 4.0, gl.FLOAT, false, 0, 0);
        #     Get the location of the "modelViewMatrix" uniform variable from the
        #     shader program
        uModelViewMatrix = self.prog.uniform('modelViewMatrix')
        #     Get the location of the "perspectiveMatrix" uniform variable from the
        #     shader program
        uPerspectiveMatrix = self.prog.uniform('perspectiveMatrix')
        #     Set the values
        glUniformMatrix4fv(uModelViewMatrix, 1, GL_FALSE, perspectiveMatrix)
        glUniformMatrix4fv(uPerspectiveMatrix, 1, False, modelViewMatrix)

        #  gl.varyingVector4fv(
        #     Draw the triangles in the vertex buffer. The first parameter specifies what
        #     drawing mode to use. This can be GL_POINTS, GL_LINE_STRIP, GL_LINE_LOOP,
        #     GL_LINES, GL_TRIANGLE_STRIP, GL_TRIANGLE_FAN, GL_TRIANGLES, GL_QUAD_STRIP,
        #     GL_QUADS, and GL_POLYGON
        # gl.drawArrays( gl.LINES, 0, numLines );
        # gl.flush();

        # setInterval( drawScene, 1000 / 40 );

    #     animate();

        print('vertices', len(self.vertices), self.vertices.itemsize, self.vertices.buffer_info())
        print('vels', len(self.velocities), self.velocities.itemsize, self.velocities.buffer_info())


    # function animate() {
    #     requestAnimationFrame( animate );
    #     drawScene();
    # }


    def draw(self):
        vertices = self.vertices
        velocities = self.velocities

        # print('draw()')

        n = len(vertices)

        # count = 0
        # if self.touched:
        #     print('touch', self.touchX, self.touchY)

        ratio = self.ratio
        sqrt = math.sqrt
        touched = self.touched
        if touched:
            touchX = self.touchX
            touchY = self.touchY

        for i in range(0, self.NUM_LINES, 2):
            bp = i*3
            # copy old positions
            vertices[bp] = vertices[bp+3]
            vertices[bp+1] = vertices[bp+4]

            # inertia
            velocities[bp] *= velocities[bp+2]
            velocities[bp+1] *= velocities[bp+2]

            # horizontal
            p = vertices[bp+3]
            p += velocities[bp]
            if p < -ratio:
                p = -ratio
                velocities[bp] = abs(velocities[bp])
            elif p > ratio:
                p = ratio
                velocities[bp] = -abs(velocities[bp])

            vertices[bp+3] = p

            # vertical
            p = vertices[bp+4]
            p += velocities[bp+1]
            if p < -1:
                p = -1
                velocities[bp+1] = abs(velocities[bp+1])
            elif p > 1:
                p = 1
                velocities[bp+1] = -abs(velocities[bp+1])

            vertices[bp+4] = p

            if touched:
                dx = touchX - vertices[bp]
                dy = touchY - vertices[bp+1]
                d = sqrt(dx * dx + dy * dy)

                if d < 1:
                    if d < .05:
                        vertices[bp+3] = (random() * 2 - 1) * ratio
                        vertices[bp+4] = random() * 2 - 1
                        velocities[bp] = 0
                        velocities[bp+1] = 0

                    else:
                        dx /= d
                        dy /= d
                        d = ( 2 - d ) / 2
                        d *= d
                        velocities[bp] += dx * d * .01
                        velocities[bp+1] += dy * d * .01

        glLineWidth(5)
        addr, size = vertices.buffer_info()
        glBufferData(GL_ARRAY_BUFFER, size * vertices.itemsize, addr, GL_DYNAMIC_DRAW)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # gl.drawArrays( gl.LINES_STRIP, 0, numLines )
        glDrawArrays(GL_LINES, 0, self.NUM_LINES)
        # gl.drawArrays( gl.QUAD_STRIP, 0, numLines )

        glFlush()


# EOF
