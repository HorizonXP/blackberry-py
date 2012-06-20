// Implementation of a typical top-swipe menu for BB10

import QtQuick 1.1

Rectangle {
    id: topmenu

    property real modalAlpha: 0.7

    width: parent.width
    height: 200

    y: -height
    z: 10
    color: "lightgrey"

    Behavior on y { PropertyAnimation { duration: 700; easing.type: Easing.OutExpo } }

    function toggle() {
        if (state == "displayed")
            state = "";
        else
            state = "displayed";
    }

    states: State {
        name: "displayed"

        PropertyChanges {
            target: topmenu
            y: 0
        }
        PropertyChanges {
            target: intercept
            opacity: modalAlpha
            visible: true
        }
    }

    MouseArea {
        anchors.fill: parent
        onClicked: {
            // ignored, so that it doesn't pass through to underlying
            // controls like a Flickable
        }
    }

    Rectangle {
        id: intercept
        width: parent.width
        y: parent.height
        height: parent.parent.height
        visible: false
        color: "black"
        opacity: 0
        z: -1

        Behavior on opacity { PropertyAnimation { duration: 700; easing.type: Easing.OutExpo } }

        MouseArea {
            anchors.fill: parent
            onClicked: {
                topmenu.toggle()
            }
        }
    }
}

