
#ifndef _FONTS_H
#define _FONTS_H

#include <EGL/egl.h>
#include <GLES2/gl2.h>


#define FONT_CHARS 128

typedef struct font_support_t {
    EGLDisplay  egl_disp;
    EGLSurface  egl_surf;
    GLuint      program;
    GLuint      u_transform;
    GLuint      u_texture;
    GLuint      u_color;
    GLuint      a_position;
    GLuint      a_texcoord;
}   FontSupport;


typedef struct font_t {
    float       pt;
    GLuint      texture_id;
    float       advance[FONT_CHARS];
    float       width[FONT_CHARS];
    float       height[FONT_CHARS];
    float       tex_x1[FONT_CHARS];
    float       tex_x2[FONT_CHARS];
    float       tex_y1[FONT_CHARS];
    float       tex_y2[FONT_CHARS];
    float       offset_x[FONT_CHARS];
    float       offset_y[FONT_CHARS];
}   Font;


#define FONT_OK                 0
#define FONT_BAD_PATH           1
#define FONT_FREETYPE_ERROR     2
#define FONT_MEMORY_ERROR       3


int font_load(Font * font, const char * font_file, int point_size, int dpi);
void font_render_text(FontSupport * support, Font * font, const char * msg, float x, float y,
    float angle,
    float r, float g, float b, float a);
void font_measure_text(Font * font, const  char * msg, float * width, float * height);


#endif
