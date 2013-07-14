'''Python Open GL ES 2.0 drawing framework.'''

import threading

# Thread-local storage, basically acts as per-thread globals.
# This technique, though it generally isn't the best design,
# does provide a good fit with the OpenGL model of using
# an implicit per-thread context.
context = threading.local()
