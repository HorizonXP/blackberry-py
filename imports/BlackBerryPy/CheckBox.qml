// Reimplementation of a checkbox based on bb::cascades::CheckBox

import QtQuick 1.1

Item {
    property alias label: thelabel.text
    property bool checked: false

    signal checkedChanged(bool changed)

    function setChecked(new_checked) {
        checked = new_checked;
    }

    function resetChecked() {
        checked = false;
    }

    function isChecked() {
        return checked;
    }

    Row {
        id: tap_area

        height: childrenRect.height
        width: childrenRect.width

        spacing: 10

        Image {
            id: show_pass
            source: checked ? "checkbox_checked.png" : "checkbox_unchecked.png"
            visible: true
        }

        Text {
            id: thelabel

            anchors.verticalCenter: show_pass.verticalCenter

            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            text: "Look at me! I'm a freakin' SWIPE_DOWN menu!"
            wrapMode: Text.WordWrap
            font.pointSize: 24
        }

    }

    MouseArea {
        anchors.fill: tap_area
        onClicked: {
            checked = !checked;
            checkedChanged(checked)
        }
    }

    Rectangle {
        anchors.fill: tap_area
        border.width: 1
        border.color: "red"
        color: "pink"
        opacity: 0.3
        visible: typeof(debug_outlines) != "undefined" && debug_outlines
    }
}
