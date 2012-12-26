precision mediump float;

uniform sampler2D s_texture;

void main() {
    gl_FragColor = texture2D(s_texture, gl_PointCoord);
}
