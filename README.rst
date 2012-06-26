The BlackBerry-Py Project
==========================
Courtesy of the BB-Py Project team (see CREDITS), and one or more unnamed
individuals at RIM who had the good sense, motivation, and ability to add
a Python 3.2 runtime into the PlayBook 2.0 OS and not hide it from developers.

More to come here... for now, please note that this is copyrighted software
that can be used only under certain legal terms as described in the file
legal/LICENSE.

Feature Support Matrix
-----------------------
The following table shows the current status of support for various
PlayBook/BB10 features in the BlackBerry-Py package.

Not explicitly mentioned are all those awesome packages and features
already bundled in the "batteries-included" Python standard library,
including networking, filesystem access, SQLite,
threading and multi-processing,
piles of text parsing and data processing options (JSON, XML, etc),
and of course the excellent ctypes package which will let you "wrap"
just about any C .so library.

And if something's missing, just find an existing pure Python package,
or port one that has some binary component to it (most shouldn't be
difficult to port).  There are thousands of such packages that are
very useful and, often, with non-restrictive open source licences.

.. list-table:: Status of feature support (preliminary)
    :widths: 25,10,65
    :header-rows: 1

    * - Feature
      - Supported?
      - Notes
    * - Accelerometer
      - NO
      - easily added with ctypes wrapper
    * - App state (active, inactive)
      - SOON
      - in progress
    * - Audio (play .wav files)
      - YES
      - via on-device qnx.audio package
    * - Bezel-swipe/top-swipe event
      - YES
      - in bbpy.Application and QML
    * - Camera
      - NO
      - can be added with ctypes wrapper
    * - Device Info (e.g. PIN)
      - YES
      - via on-device qnx.device package
    * - Dialogs
      - YES
      - via on-device qnx.dialog package
    * - File Storage
      - YES
      - all Python, QML, Qt supported
    * - Geolocation
      - YES
      - via on-device qnx.geolocation package (with hot-patch)
    * - Keyboard (virtual)
      - YES
      - handles size automatically
    * - Keyboard (predictive)
      - NO
      - may require Qt5 (future)
    * - LED
      - YES
      - via on-device qnx.led package (not tested recently)
    * - NFC
      - SOON
      - in progress, via ctypes wrapper
    * - Notifications
      - YES
      - via on-device qnx.notification package
    * - Orientation
      - YES
      - via Qt display resizing
    * - User Interface
      - YES
      - full QtQuick (QML) support
    * - Window state (hidden, thumbnail, fullscreen)
      - SOON
      - in progress

If there's something you think should be in the above list,
remember that this is a community-driven project. Just let
us know (@BBPyProject or BBPyProject at gmail dot com) and
we can add it!
