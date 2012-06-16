import QtQuick 1.1

Rectangle {
    id: root
    color: "lightsteelblue"

    // uncomment for interactive testing
    /* Component.onCompleted: {
    }*/

    Rectangle {
        id: instructions

        width: parent.width
        height: parent.height * 0.4
        color: "#000"

        Text {
            anchors.fill: parent
            anchors.margins: 12
            color: "white"
            font.family: "Zapfino"
            font.pointSize: 18
            wrapMode: Text.WordWrap

            text: "<u><h3>BlackBerry-Py Dialog Sample</h3></u>" +
                "<p>This utility is a sample to demonstrate how to " +
                "use dialogs with the BB-Py package."
        }
    }

    Flow {
        width: parent.width

        anchors.left: parent.left
        anchors.top: instructions.bottom

        anchors.margins: 10
        spacing: 10

        Button {
            height: 70
            text: "Popup"

            onButtonClicked: {
                engine.do_dialog({
                    type: 'alert',
                    messageText: 'this is my text'
                })
            }
        }
    }
}
