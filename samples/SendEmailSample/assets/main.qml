import bb.cascades 1.0
import "tart.js" as Tart

NavigationPane {
    id: root

    property variant to_list: ['BBPyProject@gmail.com']
    property string subject: 'Test email from Send Email sample.'
    property string body: 'Hello there, things are great here!'
    property variant attachment_list: []

    Page {
        id: mainPage

        Container {
            verticalAlignment: VerticalAlignment.Center

            Label {
                id: label
                horizontalAlignment: HorizontalAlignment.Center
                multiline: true
                text: qsTr("Send an email")
                textStyle.fontSize: FontSize.PercentageValue
                textStyle.fontSizeValue: 150
                textStyle.textAlign: TextAlign.Center
            }

            Button {
                horizontalAlignment: HorizontalAlignment.Center
                enabled: attachment_list.length

                text: qsTr("via Python")
                onClicked: {
                    Tart.send('testInvoke', {data: email.getData()});
                }
            }

            Button {
                horizontalAlignment: HorizontalAlignment.Center
                enabled: attachment_list.length

                text: qsTr("via C++")
                onClicked: {
                    app.composeEmail(query);
                }
            }
        }

        actions: [
            // This is a simpler technique but it doesn't allow specifying
            // all fields, and can't do attachments. There's an alternate
            // form that can do attachments but no other fields.
            InvokeActionItem {
                title: qsTr("Send")
                ActionBar.placement: ActionBarPlacement.OnBar
                query {
                    invokeActionId: 'bb.action.SENDEMAIL'
                    invokeTargetId: 'sys.pim.uib.email.hybridcomposer'
                    uri: 'mailto:BBPyProject@gmail.com'
                }
            }
        ]
    }

    attachedObjects: [
        InvokeQuery {
            id: query
            property bool ready: query.data != ''

            invokeActionId: 'bb.action.COMPOSE'
            mimeType: 'message/rfc822'

            data: JSON.stringify({
                to: to_list,
                subject: subject,
                body: body,
                attachment: attachment_list
            })

            onDataChanged: {
                print('new query data', data);
            }
        }
        ,
        QtObject {
            id: email
            property bool ready: false

            function getData() {
                return JSON.stringify({
                    to: to_list,
                    subject: subject,
                    body: body,
                    attachment: attachment_list
                });
            }
        }
    ]

    function onFilePathUpdated(data) {
        print('path updated', data.path);
        attachment_list = data.paths;
    }

    onCreationCompleted: {
        // Tart.debug = true;
        Tart.init(_tart, Application);

        Tart.register(root);

        Tart.send('uiReady');
    }
}
