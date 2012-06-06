import QtQuick 1.1

Rectangle {
    id: root
    width: 1024
    height: 600
    color: "lightsteelblue"

    states: State {
        name: "portrait"
        when: width < height

        PropertyChanges {
            target: instructions
            width: root.width
            height: 440
        }
        PropertyChanges {
            target: chooser
            anchors.topMargin: 25
            anchors.bottomMargin: 25
            anchors.leftMargin: (parent.width - width) / 2
        }
        AnchorChanges {
            target: chooser
            anchors.left: instructions.left
            anchors.top: instructions.bottom
            anchors.bottom: parent.bottom
            anchors.verticalCenter: undefined
        }
    }

    function onFileListChanged(items) {
        chooser.display(items);
    }

    function onFileLoaded(path) {
        chooser.visible = false;
    }

    // uncomment for interactive testing
    /* Component.onCompleted: {
        chooser.display(['.. (parent folder)',
            'test/',
            'this/',
            'folder/',
            'now_whatever/',
            'SomeClasses/',
            'fake.qml',
            'Dummy.qml',
            'AnotherFolder/',
            'MyFileList.qml',
            '_main.qml'
            ])
    }*/

    Rectangle {
        id: instructions

        width: 400
        height: parent.height
        color: "#000"

        Text {
            anchors.fill: parent
            anchors.margins: 12
            color: "white"
            font.family: "Zapfino"
            font.pointSize: 18
            wrapMode: Text.WordWrap

            text: "<u><h3>BlackBerry-Py QMLView</h3></u>" +
                "<p>This utility is a sample to demonstrate how to " +
                "write apps using PySide and QML with the BB-Py package." +
                "<p>Copy your QML file(s) to the shared/misc folder " +
                "and select it in the file chooser.  Then edit the file " +
                "over the WiFi or USB connection using a text editor on your PC." +
                "<p>The display will update when you save, and errors will be " +
                "shown in a special page."
        }
    }

    Rectangle {
        id: chooser

        border.width: 3
        radius: 10
        width: 400
        height: parent.height - 50
        anchors.left: instructions.right
        anchors.leftMargin: (parent.width - instructions.width - width) / 2
        anchors.verticalCenter: parent.verticalCenter
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
                color: ((index % 2 == 0) ? "#222" : "#555")
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
            anchors.topMargin: 5 + parent.border.width
            anchors.bottom: parent.bottom
            anchors.bottomMargin: 5
            anchors.horizontalCenter: parent.horizontalCenter
            clip: true

            delegate: filesDelegate
            model: filesModel
        }
    }
}
