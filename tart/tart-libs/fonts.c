/*
 * Copyright (c) 2011-2012 Research In Motion Limited.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#include <stdbool.h>
#include <math.h>

#include "fonts.h"

#include <ft2build.h>
#include FT_FREETYPE_H

#include "debug.h"


//-----------------------------------------------
// Finds the next power of 2
//
static inline int
nextp2(int x)
{
    int val = 1;
    while (val < x)
        val <<= 1;
    return val;
}


//-----------------------------------------------
//
int font_load(Font * font, const char * path, int point_size, int dpi) {
    FT_Library library;
    FT_Face face;
    int c;
    int i, j;

    log_debug("font_load %s %d %d", path, point_size, dpi);

    if (!path){
        // fprintf(stderr, "Invalid path to font file\n");
        return FONT_BAD_PATH;
    }

    if (FT_Init_FreeType(&library)) {
        // fprintf(stderr, "Error loading Freetype library\n");
        return FONT_FREETYPE_ERROR;
    }
    if (FT_New_Face(library, path, 0, &face)) {
        // fprintf(stderr, "Error loading font %s\n", path);
        return FONT_FREETYPE_ERROR;
    }

    if (FT_Set_Char_Size(face, point_size * 64, point_size * 64, dpi, dpi)) {
        // fprintf(stderr, "Error initializing character parameters\n");
        return FONT_FREETYPE_ERROR;
    }

    font->pt = point_size;

    glGenTextures(1, &(font->texture_id));

    //Let each glyph reside in 32x32 section of the font texture
    int segment_size_x = 0, segment_size_y = 0;
    int num_segments_x = 16;
    int num_segments_y = 8;

    FT_GlyphSlot slot;
    FT_Bitmap bmp;
    int glyph_width, glyph_height;

    //First calculate the max width and height of a character in a passed font
    for (c = 0; c < 128; c++) {
        if(FT_Load_Char(face, c, FT_LOAD_RENDER)) {
            // fprintf(stderr, "FT_Load_Char failed\n");
            return FONT_FREETYPE_ERROR;
        }

        slot = face->glyph;
        bmp = slot->bitmap;

        glyph_width = bmp.width;
        glyph_height = bmp.rows;

        if (glyph_width > segment_size_x)
            segment_size_x = glyph_width;

        if (glyph_height > segment_size_y)
            segment_size_y = glyph_height;
    }

    int texture_width = nextp2(num_segments_x * segment_size_x);
    int texture_height = nextp2(num_segments_y * segment_size_y);

    // fprintf(stderr, "texture width %d, height %d\n", texture_width, texture_height);

    int bitmap_offset_x = 0, bitmap_offset_y = 0;

    // The 2 * size here seems likely to be because with GL_LUMINANCE_ALPHA
    // we have two bytes, each with the same data.
    GLubyte * texture_data = (GLubyte *)
        calloc(2 * texture_width * texture_height, sizeof(GLubyte));

    if (!texture_data) {
        // fprintf(stderr, "Failed to allocate memory for font texture\n");
        return FONT_MEMORY_ERROR;
    }

    // Fill font texture bitmap with individual bmp data and record appropriate size,
    // texture coordinates and offsets for every glyph
    for (c = 0; c < FONT_CHARS; c++) {
        // if (FT_Load_Char(face, c < 127 ? c : 0x2113, FT_LOAD_RENDER)) {
        if (FT_Load_Char(face, c, FT_LOAD_RENDER)) {
            // fprintf(stderr, "FT_Load_Char failed\n");
            return FONT_FREETYPE_ERROR;
        }

        slot = face->glyph;
        bmp = slot->bitmap;

        glyph_width = bmp.width;
        glyph_height = bmp.rows;

        div_t temp = div(c, num_segments_x);

        bitmap_offset_x = segment_size_x * temp.rem;
        bitmap_offset_y = segment_size_y * temp.quot;

        for (j = 0; j < glyph_height; j++) {
            for (i = 0; i < glyph_width; i++) {
                GLubyte data = (i >= bmp.width || j >= bmp.rows)
                    ? 0
                    : bmp.buffer[i + bmp.width * j];

                int offset = 2 * ((bitmap_offset_x + i)
                    + (j + bitmap_offset_y) * texture_width);

                texture_data[offset] = texture_data[offset + 1] = data;
            }
        }

        font->advance[c] = (float)(slot->advance.x >> 6);
        font->tex_x1[c] = (float)bitmap_offset_x / (float) texture_width;
        font->tex_x2[c] = (float)(bitmap_offset_x + bmp.width) / (float)texture_width;
        font->tex_y1[c] = (float)bitmap_offset_y / (float) texture_height;
        font->tex_y2[c] = (float)(bitmap_offset_y + bmp.rows) / (float)texture_height;
        font->width[c] = bmp.width;
        font->height[c] = bmp.rows;
        font->offset_x[c] = (float)slot->bitmap_left;
        font->offset_y[c] = (float)((slot->metrics.horiBearingY
            - face->glyph->metrics.height) >> 6);
    }

    glBindTexture(GL_TEXTURE_2D, font->texture_id);
    glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR);
    glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR);

    glTexImage2D(GL_TEXTURE_2D, 0, GL_LUMINANCE_ALPHA, texture_width, texture_height, 0,
        GL_LUMINANCE_ALPHA , GL_UNSIGNED_BYTE, texture_data);

    free(texture_data);

    FT_Done_Face(face);
    FT_Done_FreeType(library);

    return FONT_OK;
}


//-----------------------------------------------
//
void font_render_text(FontSupport * support, Font * font,
    const char * msg,
    float x, float y,
    float rotation,
    float r, float g, float b, float a)
    {
    int i, c;
    GLfloat * vertices;
    GLfloat * matrix;
    GLfloat * texture_coords;
    GLushort * indices;

    float pen_x = 0.0f;

    if (!support || !font) {
        return;
    }

    if (!msg) {
        return;
    }

    const int msg_len = strlen(msg);

    vertices = (GLfloat*) malloc(sizeof(GLfloat) * 8 * msg_len);
    texture_coords = (GLfloat*) malloc(sizeof(GLfloat) * 8 * msg_len);
    indices = (GLushort*) malloc(sizeof(GLushort) * 6 * msg_len);
    matrix = (GLfloat*) malloc(sizeof(GLfloat) * 16);

    for (i = 0; i < msg_len; ++i) {
        c = msg[i];

        vertices[8 * i + 0] = pen_x + font->offset_x[c];
        vertices[8 * i + 1] = font->offset_y[c];
        vertices[8 * i + 2] = vertices[8 * i + 0] + font->width[c];
        vertices[8 * i + 3] = vertices[8 * i + 1];
        vertices[8 * i + 4] = vertices[8 * i + 0];
        vertices[8 * i + 5] = vertices[8 * i + 1] + font->height[c];
        vertices[8 * i + 6] = vertices[8 * i + 2];
        vertices[8 * i + 7] = vertices[8 * i + 5];

        texture_coords[8 * i + 0] = font->tex_x1[c];
        texture_coords[8 * i + 1] = font->tex_y2[c];
        texture_coords[8 * i + 2] = font->tex_x2[c];
        texture_coords[8 * i + 3] = font->tex_y2[c];
        texture_coords[8 * i + 4] = font->tex_x1[c];
        texture_coords[8 * i + 5] = font->tex_y1[c];
        texture_coords[8 * i + 6] = font->tex_x2[c];
        texture_coords[8 * i + 7] = font->tex_y1[c];

        indices[i * 6 + 0] = 4 * i + 0;
        indices[i * 6 + 1] = 4 * i + 1;
        indices[i * 6 + 2] = 4 * i + 2;
        indices[i * 6 + 3] = 4 * i + 2;
        indices[i * 6 + 4] = 4 * i + 1;
        indices[i * 6 + 5] = 4 * i + 3;

        //Assume we are only working with typewriter fonts
        pen_x += font->advance[c];
    }

    glEnable(GL_BLEND);

    EGLint surface_width = 1, surface_height = 1;
    eglQuerySurface(support->egl_disp, support->egl_surf, EGL_WIDTH, &surface_width);
    eglQuerySurface(support->egl_disp, support->egl_surf, EGL_HEIGHT, &surface_height);
    // fprintf(stderr, "surface width %d, surface height %d\n", surface_width, surface_height);

    // Render text
    glUseProgram(support->program);

    float angle = rotation * M_PI / 180.0f;

    // Map text coordinates from (0...surface width, 0...surface height) to
    // (-1...1, -1...1).  This make our vertex shader very simple and also
    // works irrespective of orientation changes.
    matrix[0] = 2.0 / surface_width * cos(angle);
    matrix[1] = 2.0 / surface_height * -sin(angle);
    matrix[2] = 0.0f;
    matrix[3] = 0.0f;
    matrix[4] = 2.0 / surface_width * sin(angle);
    matrix[5] = 2.0 / surface_height * cos(angle);
    matrix[6] = 0.0f;
    matrix[7] = 0.0f;
    matrix[8] = 0.0f;
    matrix[9] = 0.0f;
    matrix[10] = 1.0f;
    matrix[11] = 0.0f;
    matrix[12] = -1.0f + 2 * x / surface_width;
    matrix[13] = -1.0f + 2 * y / surface_height;
    matrix[14] = 0.0f;
    matrix[15] = 1.0f;
    glUniformMatrix4fv(support->u_transform, 1, false, matrix);

    glBlendFunc(GL_ONE, GL_ONE_MINUS_SRC_ALPHA);

    glBindBuffer(GL_ARRAY_BUFFER, 0);

    glActiveTexture(GL_TEXTURE0);
    glBindTexture(GL_TEXTURE_2D, font->texture_id);

    glUniform1i(support->u_texture, 0);
    glUniform4f(support->u_color, r, g, b, a);

    glEnableVertexAttribArray(support->a_position);
    glVertexAttribPointer(support->a_position, 2, GL_FLOAT, GL_FALSE, 0, vertices);

    glEnableVertexAttribArray(support->a_texcoord);
    glVertexAttribPointer(support->a_texcoord, 2, GL_FLOAT, GL_FALSE, 0, texture_coords);

    // Draw the string
    glDrawElements(GL_TRIANGLES, 6 * msg_len, GL_UNSIGNED_SHORT, indices);

    glDisableVertexAttribArray(support->a_position);
    glDisableVertexAttribArray(support->a_texcoord);

    free(vertices);
    free(texture_coords);
    free(indices);
    free(matrix);
}


//-----------------------------------------------
//
void font_measure_text(Font * font,
    const char * msg, float * width, float * height) {

    int i, c;

    if (!font || !msg) {
        if (width) *width = 0.0f;
        if (height) *height = 0.0f;
        return;
    }

    const int msg_len = strlen(msg);

    // Width of a text rectangle is sum of advances for every glyph in a string
    if (width) {
        *width = 0.0f;

        for (i = 0; i < msg_len; ++i) {
            c = msg[i];
            *width += font->advance[c];
        }
    }

    // Height of a text rectangle is height of tallest glyph in a string
    if (height) {
        *height = 0.0f;

        for (i = 0; i < msg_len; ++i) {
            c = msg[i];

            if (*height < font->height[c]) {
                *height = font->height[c];
            }
        }
    }
}


// EOF
