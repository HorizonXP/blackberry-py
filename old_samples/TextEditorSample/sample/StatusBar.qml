import QtQuick 1.1

Rectangle {
    id: status

    property bool changed: false
    property string filepath: ''

    property int row: -1
    property int col: -1

    Row {
        anchors.fill: parent
        anchors.margins: 5

        StatusItem {
            id: statrow
            width: parent.width * 0.15
            label: 'Row:'
            text: row
        }

        StatusItem {
            id: statcol
            width: parent.width * 0.15
            label: 'Col:'
            text: col
        }

        StatusItem {
            id: statpath
            width: parent.width - x
            label: 'File:'
            text: filepath
        }
    }

    Component.onCompleted: {
        if (liveview)
            status.filepath = '/accounts/1000/shared/misc/this/is/a/really/longer/fodler/path//a/really/longer/fodler/path/hat/goes/on/and/on/myfile.txt'
    }
}

