import QtQuick 1.1
import BlackBerryPy 0.9

Rectangle {
    width: 1024
    height: 600

    Row {
        height: parent.height
        spacing: 10

        Text {
            text: "Image right here -->"
            anchors.verticalCenter: parent.verticalCenter
        }

        Image {
            source: "http://www.engcorp.com/apps/bgsmall.png"
            anchors.verticalCenter: parent.verticalCenter
        }
    }
}
