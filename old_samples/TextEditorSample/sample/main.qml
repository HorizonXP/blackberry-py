import QtQuick 1.1
import BlackBerryPy 0.9

Rectangle {
    id: root

    signal fileListChanged(string folder, variant items)
    onFileListChanged: {
        console.log('list changed', items.length, 'items');
        chooser.display(folder, items);
    }

    signal fileLoaded(string path, string text)
    onFileLoaded: {
        console.log('file loaded', path);
        chooser.visible = false;
        edit_panel.text = text;
        status.filepath = path;
        status.changed = false;
    }

    Component.onCompleted: {
        editor.fileListChanged.connect(fileListChanged);
        editor.fileLoaded.connect(fileLoaded);
    }

    KeyboardProxy {
        id: kb

        /* showing: true
        y: 600-244
        height: 244 */

        onShowingChanged: {
            console.log('showing?', kb.showing);
        }
    }

    Image {
        id: background
        source: "../assets/background.jpg"
        fillMode: Image.PreserveAspectCrop
        anchors.fill: parent
        opacity: 0.4
    }

    EditPanel {
        id: edit_panel

        anchors.bottom: status.top
    }

    StatusBar {
        id: status

        row: edit_panel.cursorRow
        col: edit_panel.cursorCol

        anchors.bottom: kb.showing ? kb.top : buttons.top
        anchors.bottomMargin: kb.showing ? 0 : 5
        width: parent.width
        height: 20

        color: "#a0ffffff"
    }

    Row {
        id: buttons

        x: 5
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 5
        height: 60

        spacing: 10

        Button {
            text: "New"
            onButtonClicked: {
                editor.do_new();
            }
        }

        Button {
            text: "Load"
            onButtonClicked: {
                editor.do_get_filelist();
            }
        }

        Button {
            text: "Save"
            onButtonClicked: {
                console.log('saving', edit_panel.text.length);
                editor.do_save(edit_panel.text);
            }
        }

        /* Button {
            text: "Save As"
            onButtonClicked: {
                editor.do_dialog('saveas');
            }
        } */
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

    FileChooser {
        id: chooser

        onAccepted: {
            console.log('accepted: load', name);
            editor.do_select(name);
        }
    }
}
