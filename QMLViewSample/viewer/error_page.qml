import QtQuick 1.0

Rectangle {
    id: root

    width: 1024
    height: 600

    border.width: 1
    color: "#804488aa"

    /* FIXME: PySide crashes when I try this whole approach. :(

    signal returnHome()

    Rectangle {
        id: button

        property alias text: textItem.text

        height: 70
        width: 150
        border.width: 1
        radius: 5
        smooth: true

        gradient: Gradient {
            GradientStop { position: 0.0; color: "darkGray" }
            GradientStop { position: 0.5; color: "black" }
            GradientStop { position: 1.0; color: "darkGray" }
        }

        Text {
            id: textItem
            anchors.centerIn: parent
            font.pointSize: 20
            color: "white"
            text: "Pick File"
        }

        MouseArea {
            id: mouseArea
            anchors.fill: parent

            onClicked: {
                console.log('---------------------------')
                console.log('clicked', textItem.text)
                root.returnHome();
                console.log('returned from returnHome()');
            }
        }
    }
    */

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

