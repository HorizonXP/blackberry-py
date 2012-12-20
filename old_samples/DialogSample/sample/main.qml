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
            text: "Alert"

            onButtonClicked: {
                engine.do_dialog({
                    type: 'alert',
                    messageText: 'this is my text'
                })
            }
        }

        // TODO:
        // type: 'certificate_details'
        // type: 'certification_verification'

        Button {
            height: 70
            text: "ContextMenu"

            onButtonClicked: {
                engine.do_dialog({
                    type: 'context_menu',
                    messageText: 'this is my text'
                })
            }
        }

        Button {
            height: 70
            text: "FileBrowse"

            onButtonClicked: {
                engine.do_dialog({
                    type: 'file_browse',
                    messageText: 'this is my text',
                    filter: ['*.py', '*.qml', '*.txt'],
                    buttons: [{label: 'CANCEL'}, {label: 'OK'}]
                })
            }
        }

        Button {
            height: 70
            text: "FileSave"

            onButtonClicked: {
                engine.do_dialog({
                    type: 'file_save',
                    messageText: 'this is my text'
                })
            }
        }

        Button {
            height: 70
            text: "Login"

            onButtonClicked: {
                engine.do_dialog({
                    type: 'login',
                    messageText: 'this is my text'
                })
            }
        }

        Button {
            height: 70
            text: "Prompt"

            onButtonClicked: {
                engine.do_dialog({
                    type: 'prompt',
                    messageText: 'this is my text'
                })
            }
        }
    }
}
