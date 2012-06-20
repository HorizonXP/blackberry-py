import QtQuick 1.0

Rectangle {
    id: root

    width: 1024
    height: 600

    border.width: 1
    color: "#804488aa"

    // FIXME: PySide crashes when I try this whole approach. :(
    signal returnHome()
    Rectangle {
        id: button
        color: "transparent"
        height: 1
        width: 1

        MouseArea {
            id: mouseArea
            anchors.fill: parent

            onClicked: {
                root.returnHome();
            }
        }
    }

    Item {
        anchors.top: button.bottom
        anchors.topMargin: 50
        width: parent.width

        Text {
            id: errorText
            anchors.fill: parent
            anchors.margins: 10
            font.pointSize: 20
            color: "white"
            wrapMode: Text.Wrap

            text: engine.errors
        }
    }
 }

