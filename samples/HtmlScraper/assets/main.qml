import bb.cascades 1.0
import "../tart.js" as Tart


Page {
    id: root

    Container {
        Label {
            id: label
            multiline: true
            text: qsTr("Hit Load to get the news")
            visible: text
        }

        ListView {
            id: theList

            dataModel: ArrayDataModel {
                id: theModel
            }

            listItemComponents: [
                ListItemComponent {
                    type: ''    // the default if itemType() not defined on ListView

                    StandardListItem {
                        title: ListItemData.title
                        description: ListItemData.url
                    }
                }
            ]
        }
    }

    function onAddStories(data) {
        label.text = '';

        var stories = data.stories;
        for (var i = 0; i < stories.length; i++) {
            var story = stories[i];
            theModel.append({title: story[0], url: story[1]})
        }
    }

    actions: [
        ActionItem {
            title: qsTr("Load")

            ActionBar.placement: ActionBarPlacement.OnBar

            onTriggered: {
                Tart.send('requestPage', {source: 'news'});
                label.text = qsTr("Loading data, please wait...")
            }
        }
    ]

    onCreationCompleted: {
        Tart.init(_tart, Application);

        Tart.register(root);

        Tart.send('uiReady');
    }
}
