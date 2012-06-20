import QtQuick 1.1

Item {
    id: kb

    property bool showing: false

    // these adjust as keyboard appears and disappears,
    // and, when keyboard is visible, as device is rotated
    y: parent.height
    height: 0

    anchors.left: parent.left
    anchors.right: parent.right
    visible: false

    signal keyboardChanged(bool visible, variant size)
    onKeyboardChanged: {
        kb.showing = visible;
        kb.y = size.height;
        kb.height = parent.height - size.height;
        // console.log('kb ' + visible + ', y ' + kb.y + ', height ' + kb.height);
    }

    Component.onCompleted: {
        if (!bbpy.liveview)
            bbpy.keyboardChange.connect(keyboardChanged);
    }

    Component.onDestruction: {
        if (!bbpy.liveview)
            bbpy.keyboardChange.disconnect(keyboardChanged);
    }
}
