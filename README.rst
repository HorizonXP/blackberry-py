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
    * - Networking
      - YES
      - all standard Python support
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
