import bb.cascades 1.0
import bb.system 1.0
import "tart.js" as Tart

NavigationPane {
    id: root

    Page {
        id: page

        titleBar: TitleBar {
            title: "Zombie Slayer"
        }

        // outer container
        Container {
            background: Color.create("#121212")
            horizontalAlignment: HorizontalAlignment.Fill
            verticalAlignment: VerticalAlignment.Fill
            layoutProperties: StackLayoutProperties {
                spaceQuota: 1
            }

            // upper area with main content
            Container {
                background: Color.create("#262626")
                horizontalAlignment: HorizontalAlignment.Fill
                verticalAlignment: VerticalAlignment.Fill
                layoutProperties: StackLayoutProperties {
                    spaceQuota: 1
                }
                topPadding: 20

                layout: DockLayout {}

                // main view with list of apps
                Container {
                    visible: appModel.item_count
                    horizontalAlignment: HorizontalAlignment.Center

                    Label {
                        horizontalAlignment: HorizontalAlignment.Center
                        text: qsTr("Select an app and tap Slay to terminate it.")
                    }

                    ListView {
                        id: appList
                        visible: appModel.item_count

                        property variant selectedPath: []

                        listItemComponents: ListItemComponent {
                            StandardListItem {
                                title: ListItemData.pid
                                description: ListItemData.name
                                imageSource: ListItemData.iconpath
                                imageSpaceReserved: true
                            }
                        }

                        dataModel: ArrayDataModel {
                            id: appModel
                            property int item_count: 0

                            function update_count() {
                                item_count = size();
                            }
                            onItemAdded: update_count();
                            onItemRemoved: update_count();
                            onItemsChanged: update_count();
                        }

                        onSelectionChanged: {
                            if (selected) {
                                selectedPath = indexPath;
                            }
                            else
                                selectedPath = [];
                        }

                        onTriggered: {
                            clearSelection();
                            select(indexPath, true);
                        }

                    }// ListView
                }// view when we have any items

                // alternate view when the list is empty
                Container {
                    visible: !appModel.item_count
                    horizontalAlignment: HorizontalAlignment.Center
                    verticalAlignment: VerticalAlignment.Fill
                    layout: DockLayout {}

                    Label {
                        horizontalAlignment: HorizontalAlignment.Center
                        verticalAlignment: VerticalAlignment.Center
                        text: "<html><div style='text-align: center'>" +
                            "<p style='color: red; font-size: xx-large'>No active " +
                            "<span style='text-decoration: underline'>devMode</span> " +
                            "apps could be found.</p>" +
                            "<br/>" +
                            "<p style='font-size: x-large'>Tap <b>Refresh</b> to update the list.</p>" +
                            "</div></html>";
                        multiline: true
                    }
                }// no-items view
            }// upper container

            // lower pane to advertise the BlackBerry-Py project
            Container {
                topPadding: 10
                leftPadding: 15
                rightPadding: 15
                horizontalAlignment: HorizontalAlignment.Fill

                layout: DockLayout {}

                Label {
                    horizontalAlignment: HorizontalAlignment.Center
                    verticalAlignment: VerticalAlignment.Bottom
                    text: "<html>" +
                        "<p>This utility was provided as a public service " +
                        "by the <a href='http://blackberry-py.microcode.ca'>BlackBerry-Python</a> " +
                        "project for our fellow BB10 developers! For help go to the " +
                        "<a href='http://blackberry-py.microcode.ca/zombie-slayer.html'>Zombie Slayer Help Page</a></p></html>";
                    multiline: true
                }

                Label {
                    horizontalAlignment: HorizontalAlignment.Right
                    verticalAlignment: VerticalAlignment.Bottom
                    text: "<html>" +
                        "<p style='text-align: right; font-size: small'>Copyright 2012 Peter Hansen</p>" +
                        "</html>";
                }
            }

        }// Container for Page

        actions: [
            ActionItem {
                title: qsTr("Refresh")
                ActionBar.placement: ActionBarPlacement.OnBar
                imageSource: "refresh_icon.png"
                onTriggered: {
                    Tart.send('refreshApps');
                }
            }
            ,
            ActionItem {
                title: qsTr("Slay")
                ActionBar.placement: ActionBarPlacement.OnBar
                imageSource: "slay_icon.png"
                enabled: appList.selectedPath.length
                onTriggered: {
                    var indexPath = appList.selected();
                    var item = appModel.data(indexPath);
                    if (item.pid) {
                        Tart.send('slayApp', {pid: item.pid});
                    }
                }
            }
        ]// actions
    }// page

    Menu.definition: MenuDefinition {
        // settingsAction: SettingsActionItem {
        //     enabled: false
        //     onTriggered: {
        //     }
        // }
        helpAction: HelpActionItem {
            onTriggered: {
                invokeBrowser.trigger('bb.action.OPEN');
            }
        }
    }// menu

    attachedObjects: [
        // SystemDialog {
        //     id: suicideDialog
        //     property int target_pid
        //     title: "Yikes!"
        //     body: "Hey! You selected this app! Are you sure want to kill me?"
        //     onFinished: {
        //         if (suicideDialog.result === SystemUiResult.ConfirmButtonSelection)
        //             Tart.send('slayApp', {pid: target_pid});
        //     }
        // }
        // ,
        SystemToast {
            id: theToast
            property string pid
            body: qsTr("Process %1 was 'slayed'.").arg(pid)
        }
        ,
        Invocation {
            id: invokeBrowser

            query: InvokeQuery {
                mimeType: "text/html"
                uri: "http://blackberry-py.microcode.ca/zombie-slayer.html"
            }
        }
    ]

    function onWindowStateChanged(data) {
        print('windowState', data.state);

        // if (data.state == 'thumbnail')
        //     Tart.send('saveState'); // does nothing if no changes
    }

    function onAppSlain(data) {
        print('slain', data.pid);
        theToast.pid = data.pid;
        theToast.show();
        Tart.send('refreshApps');
    }

    function onAppsRefreshed(data) {
        var apps = data.apps;
        appModel.clear();
        appList.selectedPath = [];
        for (var i = 0; i < apps.length; i++) {
            var app = apps[i];
            var item = {
                pid: app.pid,
                name: app.name,
                iconpath: app.iconpath
            };
            // print('icon', item.iconpath);

            appModel.append(item);
        }
    }

    // function onManualExit() {
    //     Application.setCover(null); // avoids an error on exiting
    //     Tart.send('manualExit');
    // }

    onCreationCompleted: {
        OrientationSupport.supportedDisplayOrientation = SupportedDisplayOrientation.All;

        Tart.init(_tart, Application);
        Tart.register(root);

        Tart.send('uiReady');
    }
}// nav pane
