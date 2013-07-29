import bb.cascades 1.0
import bb.cascades.pickers 1.0
import "tart.js" as Tart

NavigationPane {
    id: root

    property bool portrait: true

    signal keepAwake(bool enabled)

    MainPage {
        id: mainPage
    }

    attachedObjects: [
        Page {
            id: errorPage
            objectName: 'errorPage'

            property alias msg: errMsg.text

            Container {
                topPadding: 15
                leftPadding: 15

                TextArea {
                    id: errMsg
                }
            }
        }
        ,
        OrientationHandler {
            onOrientationAboutToChange: {
                portrait = (orientation == 0);
            }
        }
        ,
        ComponentDefinition {
            id: pageDef

            onSourceChanged: {
                print('sourceChanged()', source);
                pageSourceChanged();
            }

            onError: {
                print('hasErrors()', hasErrors());
                print('errorMessage()', errorMessage);
                showErrorPage(errorMessage);
            }
        }
        ,
        FilePicker {
            id: filePicker

            title: qsTr("File Picker")
            mode: FilePickerMode.Picker // Saver, Picker, PickerMultiple, SaverMultiple
            type: FileType.Other // Document, Picture, Music, Video, Other
            // viewMode: FilePickerViewMode.Default // ListView, GridView
            // sortBy: FilePickerSortFlag.Default  // Name, Suffix, Date
            // sortOrder: FilePickerSortOrder.Default // Ascending, Descending

            directories: ['/accounts/1000/shared/misc']
            filter: ['*.qml']

            onFileSelected: {
                var path = selectedFiles[0];
                print('selected', path);
                // pageDef.source = path;

                Tart.send('monitorFile', {path: path});
            }
        }
    ]

    function onFileChanged(data) {
        print('load and create', data.path);
        pageDef.source = data.path;
    }

    function pageSourceChanged() {
        pageDef.load();
        var page = pageDef.createObject();
        if (page == null) {
            print('error creating', pageDef.hasErrors(), pageDef.errorMessage());
            showErrorPage(pageDef.errorMessage());
        }
        else
            setTopPage(page);
    }

    function setTopPage(page) {
        if (top) {
            print('pop old', top, top.objectName);
            root.pop(top);
        }

        print('push new', page);
        root.push(page);
    }

    function showErrorPage(msg) {
        errorPage.msg = msg;
        setTopPage(errorPage);
    }

    function onSwipeDown() {
        onFileChanged({path: pageDef.source});
    }

    onPopTransitionEnded: {
        print('pop ended', page);
        if (page != errorPage)
            page.destroy();
    }

    onKeepAwake: {
        // This should be enabled ? ScreenIdleMode.KeepAwake : ScreenIdleMode.Normal
        // but the enum is broken in QML
        Application.mainWindow.screenIdleMode = enabled ? 1 : 0;
    }

    onCreationCompleted: {
        // Tart.debug = true;
        Tart.init(_tart, Application);

        Tart.register(root);

        Tart.send('uiReady');

        print('hasErrors', pageDef.hasErrors());
        print('errorMessage', pageDef.errorMessage());
    }
}
