import bb.cascades 1.0
import "tart.js" as Tart

NavigationPane {
    id: root

    Page {
        id: mainPage

        Container {
            layout: DockLayout {}

            Label {
                id: label
                horizontalAlignment: HorizontalAlignment.Center
                verticalAlignment: VerticalAlignment.Center
                multiline: true
                text: qsTr("App %1 ready to evolve, sir!").arg(Application.applicationName)
                textStyle.fontSize: FontSize.XLarge
            }
        }
    }

    Menu.definition: MenuDefinition {
        helpAction: HelpActionItem {
            onTriggered: {
                root.push(helpDef.createObject());
            }
        }
    }

    attachedObjects: [
        ComponentDefinition {
            id: helpDef

            Page {
                Container {
                    Label {
                        multiline: true
                        text: qsTr("Should users need help with well-designed apps?")
                    }
                }
            }
        }
    ]

    onPopTransitionEnded: {
        page.destroy();
    }

    onCreationCompleted: {
        // Tart.debug = true;
        Tart.init(_tart, Application);

        Tart.register(root);

        Tart.send('uiReady');
    }
}
