import QtQuick 1.1
import BlackBerryPy 0.9

Rectangle {
    id: chooser

    width: 400
    height: parent.height - 50
    anchors.centerIn: parent
    z: 2

    border.width: 3
    radius: 10
    visible: false
    color: "gray"
    clip: true

    signal accepted(string name)

    Component.onCompleted: {
        if (liveview)
            display('/accounts/1000/shared/misc/FooBar/baz_blah/spam',
                '../ the/ quick/ brown/ fox/ jumps over the lazy dog'.split(' '));
    }

    function display(folder, items) {
        folderPath.text = folder;

        if (items.length) {
            filesModel.clear();
            for (var i in items) {
                var item = {name: items[i]};
                console.log('last is', items[i].substr(-1, 1));
                item.type = items[i].substr(-1, 1) == '/' ? 'dir' : 'file';
                filesModel.append(item);
            }
        }

        filelist.currentIndex = -1;
        load_button.enabled = false;

        visible = true;
    }

    Rectangle {
        id: header

        anchors.top: parent.top
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.margins: 2

        height: 30
        radius: 9

        gradient: Gradient {
            GradientStop { position: 0.0; color: "lightsteelblue" }
            GradientStop { position: 0.5; color: "white" }
            GradientStop { position: 1.0; color: "lightsteelblue" }
        }

        Text {
            id: folderPath

            x: 10
            width: parent.width - 20
            clip: true
            elide: Text.ElideLeft

            font.pointSize: 12
            font.bold: true
            color: "gray"
            anchors.verticalCenter: parent.verticalCenter
        }
    }

    ListModel { id: filesModel }

    Component {
        id: filesDelegate

        Rectangle {
            id: wrapper
            width: parent.width
            height: 55
            color: ((index % 2 == 0) ? "#20bbbbbb" : "#20777777")
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
                    console.log('item', index, 'clicked', model.name, model.type);
                    filelist.currentIndex = index;
                    if (model.type == 'dir') {
                        load_button.enabled = false;
                        editor.do_select(model.name);
                    }
                    else
                        load_button.enabled = true;
                }
            }
        }
    }

    ListView {
        id: filelist
        width: parent.width - 16

        anchors.top: header.bottom
        anchors.bottom: buttons.top
        anchors.bottomMargin: 5
        anchors.horizontalCenter: parent.horizontalCenter
        clip: true
        delegate: filesDelegate
        model: filesModel

        highlight: Rectangle { color: "blue"}
        highlightMoveSpeed: -1
        highlightMoveDuration: -1
        highlightFollowsCurrentItem: true
    }

    Row {
        id: buttons

        anchors.bottom: parent.bottom
        anchors.bottomMargin: 5
        anchors.horizontalCenter: parent.horizontalCenter
        height: 45

        spacing: 10

        Button {
            id: load_button
            text: "Load"
            enabled: false

            onButtonClicked: {
                console.log('selected', filesModel.get(filelist.currentIndex).name);
                accepted(filesModel.get(filelist.currentIndex).name);
                chooser.visible = false;
            }
        }

        Button {
            text: "Cancel"
            onButtonClicked: {
                chooser.visible = false;
            }
        }
    }
}
