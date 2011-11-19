#include <ctype.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/keycodes.h>
#include <screen/screen.h>
#include <assert.h>
#include <bps/accelerometer.h>
#include <bps/navigator.h>
#include <bps/screen.h>
#include <bps/bps.h>
#include <bps/event.h>
#include <bps/orientation.h>
#include <math.h>
#include <time.h>
#include <screen/screen.h>

#include <EGL/egl.h>
#include <GLES/gl.h>

#include "png.h"
#include "bbutil.h"
#include "pyinit.h"

static float width, height;
static GLuint background;
static GLfloat vertices[8];
static GLfloat tex_coord[8];
static screen_context_t screen_cxt;
// static float pos_x, pos_y;

static const font_t * font;


//---------------------------------------------------------
//
void handleScreenEvent(bps_event_t *event) {
    screen_event_t screen_event = screen_event_get_event(event);

    int screen_val;
    screen_get_event_property_iv(screen_event, SCREEN_PROPERTY_TYPE, &screen_val);

    switch (screen_val) {
        case SCREEN_EVENT_MTOUCH_TOUCH:
        case SCREEN_EVENT_MTOUCH_MOVE:
        case SCREEN_EVENT_MTOUCH_RELEASE:
            break;
    }
}


//---------------------------------------------------------
//
int init() {
	EGLint surface_width, surface_height;

	// On initialize bbutil loads Arial as a default font. We are going to load MyriadPro-Bold as it looks a little better and scale it
	// to fit our bubble nicely.
	int dpi = bbutil_calculate_dpi(screen_cxt);

	font = bbutil_load_font("/usr/fonts/font_repository/adobe/MyriadPro-Bold.otf", 13, dpi);
	if (!font)
		return EXIT_FAILURE;

	//Load background texture
	float tex_x, tex_y;
	if (EXIT_SUCCESS != bbutil_load_texture("app/native/background.png",
        NULL, NULL, &tex_x, &tex_y, &background)) {
		fprintf(stderr, "Unable to load background texture\n");
	}

	//Query width and height of the window surface created by utility code
	eglQuerySurface(egl_disp, egl_surf, EGL_WIDTH, &surface_width);
	eglQuerySurface(egl_disp, egl_surf, EGL_HEIGHT, &surface_height);

	EGLint err = eglGetError();
	if (err != 0x3000) {
		fprintf(stderr, "Unable to query egl surface dimensions\n");
		return EXIT_FAILURE;
	}

	width = (float) surface_width;
	height = (float) surface_height;

	//Initialize GL for 2D rendering
	glViewport(0, 0, (int) width, (int) height);

	glMatrixMode(GL_PROJECTION);
	glLoadIdentity();

	glOrthof(0.0f, width / height, 0.0f, 1.0f, -1.0f, 1.0f);

	glMatrixMode(GL_MODELVIEW);
	glLoadIdentity();

	//Set world coordinates to coincide with screen pixels
	glScalef(1.0f / height, 1.0f / height, 1.0f);

//	float text_width, text_height;
//	bbutil_measure_text(font, "Hello world", &text_width, &text_height);
//	pos_x = (width - text_width) / 2;
//	pos_y = height / 2;

	//Setup background polygon
	vertices[0] = 0.0f;
	vertices[1] = 0.0f;
	vertices[2] = width;
	vertices[3] = 0.0f;
	vertices[4] = 0.0f;
	vertices[5] = height;
	vertices[6] = width;
	vertices[7] = height;

	tex_coord[0] = 0.0f;
	tex_coord[1] = 0.0f;
	tex_coord[2] = tex_x;
	tex_coord[3] = 0.0f;
	tex_coord[4] = 0.0f;
	tex_coord[5] = tex_y;
	tex_coord[6] = tex_x;
	tex_coord[7] = tex_y;

	return EXIT_SUCCESS;
}


//---------------------------------------------------------
//
void render(const char * msg) {
	//Typical rendering pass
	glClear(GL_COLOR_BUFFER_BIT);

	//Render background quad first
	glEnable(GL_TEXTURE_2D);

	glEnableClientState(GL_VERTEX_ARRAY);
	glEnableClientState(GL_TEXTURE_COORD_ARRAY);

	glVertexPointer(2, GL_FLOAT, 0, vertices);
	glTexCoordPointer(2, GL_FLOAT, 0, tex_coord);
	glBindTexture(GL_TEXTURE_2D, background);

	glColor4f(1.0f, 1.0f, 1.0f, 1.0f);
	glDrawArrays(GL_TRIANGLE_STRIP, 0, 4);

	glDisableClientState(GL_TEXTURE_COORD_ARRAY);
	glDisableClientState(GL_VERTEX_ARRAY);
	glDisable(GL_TEXTURE_2D);

	//Set color of bbutil to use for text rendering
	glColor4f(0.35f, 0.35f, 0.35f, 1.0f);

	//Use utility code to render welcome text onto the screen
//	bbutil_render_text(font, msg, pos_x, pos_y);
	bbutil_render_text(font, msg, 10, 400);

    //Use utility code to update the screen
    bbutil_swap();
}


//---------------------------------------------------------
//
int main(int argc, char ** argv) {
    int rc;
    static screen_context_t screen_cxt;

    fprintf(stderr, "initializing\n");

    //Create a screen context that will be used to create an EGL surface to to receive libscreen events
    screen_create_context(&screen_cxt, 0);

    //Initialize BPS library
	bps_initialize();

	//Use utility code to initialize EGL for 2D rendering with GL ES 1.1
	if (EXIT_SUCCESS != bbutil_init_egl(screen_cxt, GL_ES_1, LANDSCAPE)) {
		fprintf(stderr, "Unable to initialize EGL\n");
		bbutil_terminate();
		screen_destroy_context(screen_cxt);
		return 0;
	}

	//Initialize application logic
	if (EXIT_SUCCESS != init()) {
		fprintf(stderr, "Unable to initialize app logic\n");
		bbutil_terminate();
		screen_destroy_context(screen_cxt);
		return 0;
	}

	//Signal BPS library that navigator orientation is to be locked
	if (BPS_SUCCESS != navigator_rotation_lock(true)) {
		fprintf(stderr, "navigator_rotation_lock failed\n");
		bbutil_terminate();
		screen_destroy_context(screen_cxt);
		return 0;
	}

	//Signal BPS library that navigator and screen events will be requested
	if (BPS_SUCCESS != screen_request_events(screen_cxt)) {
		fprintf(stderr, "screen_request_events failed\n");
		bbutil_terminate();
		screen_destroy_context(screen_cxt);
		return 0;
	}

	if (BPS_SUCCESS != navigator_request_events(0)) {
		fprintf(stderr, "navigator_request_events failed\n");
		bbutil_terminate();
		screen_destroy_context(screen_cxt);
		return 0;
	}

	py_initialize(argc, argv);

    const char * msg = "";
    int timeout = 0;
    for (;;) {
    	//Request and process BPS next available event
        bps_event_t *event = NULL;
        rc = bps_get_event(&event, timeout);
        assert(rc == BPS_SUCCESS);

        if (event) {
            int domain = bps_event_get_domain(event);

            if (domain == screen_get_domain()) {
                handleScreenEvent(event);
            }
            else if (   domain == navigator_get_domain()
                     && NAVIGATOR_EXIT == bps_event_get_code(event)) {
                break;
            }
        }

        render(msg);

        // stop after second time through loop
        if (timeout)
        	break;

        // usleep(100000);
        msg = py_test();
        timeout = 1000;
    }

    py_runmain();

    py_finalize();

    // stop requesting events from libscreen
    screen_stop_events(screen_cxt);

    // shut down BPS library for this process
    bps_shutdown();

	//Destroy the font
	bbutil_destroy_font(font);

    // use utility code to terminate EGL setup
    bbutil_terminate();

    // destroy libscreen context
    screen_destroy_context(screen_cxt);

    fprintf(stderr, "exiting\n");

//    FILE * logf = fopen("logs/mylog.log", "a");
//    fprintf(logf, "------------------\n");
//    fprintf(logf, "exiting\n");
//    fclose(logf);

    return 0;
}


// EOF
