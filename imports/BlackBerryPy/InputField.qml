import QtQuick 1.1

FocusScope {
    id: scope

    property alias label_text: label.text
    property alias hint_text: hint.text
    property alias text: input.text
    property alias echoMode: input.echoMode
    property alias horizontalAlignment: input.horizontalAlignment

    property bool readOnly: false

    signal accepted()

    width: parent.width
    height: rect.height

    Rectangle {
        id: rect

        width: parent.width
        height: childrenRect.height

        border.width: 0
        color: "#00ff00ff"

        Text {
            id: label

            x: 5

            color: "white"
            font.pointSize: fieldLabelSize
            font.italic: true

            text: "Label"
        }

        Rectangle {
            id: field

            anchors.top: label.bottom

            width: parent.width
            height: 55

            border.width: 4
            border.color: input.readOnly ? "transparent" : "black"
            radius: 5
            color: input.readOnly ? "darkgrey" : "white"

            TextInput {
                id: input

                anchors.centerIn: parent
                width: parent.width - 30

                color: "black"
                selectByMouse: false
                readOnly: scope.readOnly

                focus: true

                font.family: 'DejaVu Sans Mono'
                font.pointSize: fieldTextSize
                text: ''

                onAccepted: scope.accepted()
            }

            Text {
                id: hint

                anchors.left: input.left
                anchors.verticalCenter: parent.verticalCenter

                // verticalAlignment: input.verticalAlignment

                color: "lightgrey"
                visible: input.text == '' && (!input.activeFocus || input.readOnly)
                z: 1

                font.pointSize: fieldTextSize
                text: "Enter text..."
            }
        }
    }
}

