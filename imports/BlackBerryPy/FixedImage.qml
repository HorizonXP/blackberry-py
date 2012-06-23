import QtQuick 1.1

Image {
    Component.onCompleted: {
        var src = '' + source;  // ensure it's a string
        if (src) {
            objectName = src;
            if (src.substr(0, 4) == 'http') {
                bbpy.loadImageSource(src);
            }
        }
    }
}
