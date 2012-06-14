import QtQuick 1.1

Rectangle {
    id: button

    property alias text: textItem.text

    signal buttonClicked(string text)

    height: parent.height
    width: height * 2.5
    border.width: 1
    radius: 5
    smooth: true
    color: "#804488aa"

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
    }

    MouseArea {
        id: mouseArea
        anchors.fill: parent

        onClicked: {
            buttonClicked(textItem.text);
            console.log('clicked', textItem.text)
        }

        onPressed: {
            button.scale = 1.1
            button.z = 1
            textItem.font.bold = true
        }
        onReleased: {
            button.scale = 1.0
            button.z = 0
            textItem.font.bold = false
        }
    }
 }

