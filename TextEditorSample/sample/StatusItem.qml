import QtQuick 1.1

Item {
    property alias label: label.text
    property alias text: text.text

    anchors.verticalCenter: parent.verticalCenter
    height: 30
    clip: true

    Text {
        id: label
        anchors.verticalCenter: parent.verticalCenter
        text: 'Label:'
    }

    Text {
        id: text
        anchors.left: label.right
        anchors.right: parent.right
        anchors.leftMargin: 5
        anchors.verticalCenter: parent.verticalCenter

        elide: Text.ElideLeft
    }
}
