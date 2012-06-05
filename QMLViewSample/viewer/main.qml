import QtQuick 1.1

Rectangle {
    id: root
    width: 1024
    height: 600
    color: "pink"

    function onFileListChanged(items) {
        chooser.display(items);
    }

    function onFileLoaded(path) {
        chooser.visible = false;
    }

    Rectangle {
        id: ghoster
        visible: chooser.visible

        anchors.fill: root
        anchors.centerIn: root
        z: 1
        color: "black"
        opacity: 0.5
    }

    Rectangle {
        id: chooser
        border.width: 3
        radius: 10
        width: 400
        height: parent.height - 50
        anchors.centerIn: parent
        visible: false
        z: 2
        color: "gray"
        clip: true

        function display(items) {
            var folderPath = engine.folder;
            if (items.length) {
                filesModel.clear();
                for (var i in items) {
                    filesModel.append({name: items[i]})
                }
            }
            visible = true;
        }

        ListModel { id: filesModel }

        Component {
            id: filesDelegate

            Rectangle {
                width: parent.width
                height: 55
                color: ((index % 2 == 0) ? "#222" : "#444")
                Text {
                    id: filename
                    elide: Text.ElideRight
                    anchors.fill: parent
                    anchors.leftMargin: 10
                    text: model.name
                    verticalAlignment: Text.AlignVCenter
                    color: "white"
                    font.pointSize: 18
                }
                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        engine.do_select(model.name);
                    }
                }
            }
        }

        ListView {
            id: filelist
            width: parent.width - 20

            anchors.top: parent.top
            anchors.topMargin: 5
            anchors.bottom: parent.bottom
            anchors.bottomMargin: 5
            anchors.horizontalCenter: parent.horizontalCenter
            clip: true

            delegate: filesDelegate
            model: filesModel
        }
    }
}
