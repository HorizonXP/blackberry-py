import QtQuick 1.1
Rectangle {
    Text {
        anchors.centerIn: parent
        text: "This way up \u2191 (size " + parent.width + "x" + parent.height + ")"
        font.pixelSize: parent.width * 0.05
    }
}
