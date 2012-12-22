import bb.cascades 1.0
import "../tart.js" as Tart

NavigationPane {
    id: root

    property int _DEBUG: 2
    property variant chart_page

    peekEnabled: false

    Page {
        id: page

        Container {
            Label {
                text: qsTr("BB-Tart OpenGL Sample")
            }

            OglWindow {

            }
        }// Container for Page
    }

    Menu.definition: MenuDefinition {
        helpAction: HelpActionItem {
            onTriggered: {
                Tart.send('getHelp');
            }
        }
    }

    attachedObjects: [
        ComponentDefinition {
            id: helpPageDef
            source: "HelpPage.qml"
        }
    ]

    onCreationCompleted: {
        // OrientationSupport.supportedDisplayOrientation = SupportedDisplayOrientation.All;

        Tart.init(_tart, Application);

        Tart.register(root);

        Tart.send('uiReady');
    }


    //-----------------
    //
    // function onWindowStateChanged(data) {
    //     Tart.send('windowStateChanged', data);
    // }

    function onGotHelp(data) {
        var page = helpPageDef.createObject();
        page.text = data.text;
        root.push(page);
    }

}
