uniform mat4 u_mvpMatrix;
attribute vec2 a_position;

void main() {
    gl_Position = u_mvpMatrix * vec4(a_position, 0.0, 1.0);

    gl_PointSize = 64.0; // ? do we need glEnable(GL_PROGRAM_POINT_SIZE)?
}
