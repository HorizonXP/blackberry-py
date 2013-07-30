import bb.cascades 1.0
import "tart.js" as Tart

Page {
    id: mainPage

    titleBar: TitleBar {
        title: "Cuteness Overload"
    }

    Container {
        // background: Color.create('#76230f')
        layout: DockLayout {}

        ListView {
            id: theList

            dataModel: theModel

            listItemComponents: [
                ListItemComponent {
                    type: 'item'

                    StandardListItem {
                        imageSource: 'file://' + ListItemData.image
                        imageSpaceReserved: true
                        title: ListItemData.title
                        description: ListItemData.tags
                    }
                }
            ]

            function itemType() { return 'item'; }

            onTriggered: {
                var item = theModel.data(indexPath);
                print('triggered', indexPath, item.url);
                webPage.show(item);
            }

        }
    }

    actions: [
        ActionItem {
            title: "Refresh"
            ActionBar.placement: ActionBarPlacement.OnBar
            onTriggered: {
                Tart.send('refreshFeed');
            }
        }
        ,
        ActionItem {
            id: openBrowser
            enabled: root.openBrowserEnabled
            title: "Open in Browser"
            onTriggered: {
                print('open in browser', invoke.query.uri);
                invoke.trigger('bb.action.OPEN');
            }
        }
        ,
        ActionItem {
            title: "Erase data"
            onTriggered: {
                Tart.send('eraseData');
            }
        }
        ,
        ActionItem {
            title: "Fake New Item"
            onTriggered: {
                Tart.send('fakeNew');
            }
        }
    ]
}

