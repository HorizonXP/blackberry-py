import bb.cascades 1.0
import bb.platform 1.0
import bb.system 1.0
import "tart.js" as Tart


NavigationPane {
    id: root

    property bool openBrowserEnabled: false

    MainPage {
        id: mainPage
    }

    attachedObjects: [
        GroupDataModel {
            id: theModel
            sortingKeys: ['pubtime', 'link']
            sortedAscending: false
            grouping: ItemGrouping.None
        }
        ,
        Dialog {
            id: dialog

            Container {
                background: Color.Black
                horizontalAlignment: HorizontalAlignment.Fill
                verticalAlignment: VerticalAlignment.Fill

                Button {
                    text: "Close"
                    onClicked: {
                        dialog.close();
                    }
                }

                ScrollView {
                    Label {
                        id: dlgLabel
                        multiline: true
                    }
                }
            }

            function show(msg) {
                dlgLabel.text = msg;
                dialog.open();
            }
        }
        ,
        SystemToast {
            id: toast
            body: "No new items found."
        }
        ,
        ComponentDefinition {
            id: webPage

            Page {
                property alias url: webView.url
                property alias title: myTitle.title

                titleBar: TitleBar {
                    id: myTitle
                }

                ScrollView {
                    id: scrollView

                    scrollViewProperties {
                        pinchToZoomEnabled: true
                        scrollMode: ScrollMode.Both
                    }

                    WebView {
                        id: webView
                    }
                }
            }

            function show(item) {
                var page = webPage.createObject();
                page.title = item.title;
                page.url = item.url;

                root.push(page);
            }
        }
        ,
        Invocation {
            id: invoke
            query {
                invokeTargetId: 'sys.browser'
                invokeActionId: 'bb.action.OPEN'
            }

            onArmed: {
                print('invocation armed');
                openBrowserEnabled = true;
            }
        }
        ,
        Notification {
            id: alert
            title: 'Cuteness added'
            soundUrl: ''
        }
    ]

    function onPyError(data) {
        dialog.show(data.traceback);
    }

    function onEntriesLoaded(data) {
        theModel.clear();
        theModel.insertList(data.entries);
    }

    function onEntryAdded(data) {
        theModel.insert(data.entry);
        alert.body = 'New item: ' + data.entry.title;
        alert.notify();
    }

    function onNoEntriesFound(data) {
        toast.show();
    }

    function onSiteUrl(data) {
        invoke.query.uri = data.url;
        invoke.query.updateQuery();
    }

    onPopTransitionEnded: {
        page.destroy();
    }

    onCreationCompleted: {
        Tart.debug = true;
        Tart.init(_tart, Application);

        Tart.register(root);

        Tart.send('uiReady');
    }
}
