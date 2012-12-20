import QtQuick 1.1
import BlackBerryPy 0.9

Rectangle {
    id: root
    color: "#bbaaaa"

    KeyboardProxy {
        id: kb
    }

    Text {
        id: title

        width: parent.width

        font.pointSize: 22
        font.family: "DejaVu Sans"
        font.italic: true
        font.bold: true
        wrapMode: Text.Wrap
        horizontalAlignment: Text.AlignHCenter
        color: "blue"

        text: "BlackBerry-Py Keyboard Sample, with automatic size/orientation"
    }

    Item {
        id: main

        anchors.top: title.bottom
        anchors.bottom: kb.top
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.margins: 5

        Text {
            id: cons_out

            width: parent.width
            font.pointSize: 22
            font.family: "DejaVu Sans"

            text: ""
        }

        InputField {
            id: user_input_rect

            property int fieldTextSize: 22
            property int fieldLabelSize: 18

            anchors.bottom: parent.bottom
            anchors.horizontalCenter: parent.horizontalCenter
            width: parent.width - 10

            visible: kb.showing
            onVisibleChanged: {
                if (visible)
                    focus = true;
            }

            label_text: "Text what you're entering:"
            hint_text: "Enter some text..."

            onAccepted: {
                cons_out.text = 'You totally typed: ' + text;
                text = '';
            }
        }
    }

    Text {
        id: hint

        width: parent.width
        anchors.bottom: parent.bottom
        anchors.margins: 10

        visible: !kb.showing

        wrapMode: Text.Wrap
        font.pointSize: 22
        font.family: "DejaVu Sans"

        text: "\u2197 Swipe into screen from bottom-left corner to open keyboard."
    }
}
