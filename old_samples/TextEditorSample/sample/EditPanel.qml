import QtQuick 1.1
import BlackBerryPy 0.9

Rectangle {
    id: edit_panel

    property alias text: editing.text
    property alias readOnly: editing.readOnly
    property int cursorRow: getCursorRow()
    property int cursorCol: getCursorCol()

    // replaced at startup
    property int lineHeight : 1
    property int charWidth : 1

    Component.onCompleted: {
        editing.text = 'x';
        editing.cursorPosition = 1;
        charWidth = editing.cursorRectangle.x;
        lineHeight = editing.paintedHeight;
        editing.text = '';
    }

    function getCursorRow() {
        if (editing.cursorVisible)
            return editing.cursorRectangle.y / lineHeight + 1;
        else
            return -1;
    }

    function getCursorCol() {
        if (editing.cursorVisible)
            return editing.cursorRectangle.x / charWidth;
        else
            return -1;
    }

    color: false ? "#33ff2222" : "transparent"

    anchors.top: parent.top
    anchors.bottom: parent.bottom
    anchors.left: parent.left
    anchors.right: parent.right
    anchors.margins: 0

    Flickable {
        id: flick

        width: parent.width
        anchors.fill: parent

        boundsBehavior: Flickable.StopAtBounds
        pressDelay: 300

        contentHeight: column.height
        contentWidth: editing.paintedWidth
        clip: true

        Column {
            id: column
            width: parent.width
            spacing: 6

            Rectangle {
                x: flick.contentX
                width: flick.width
                height: 20
                color: "#80aaaaff"

                Text {
                    anchors.fill: parent
                    text: "(start of file)"
                    horizontalAlignment: Text.AlignHCenter
                }
            }

            Rectangle {
                id: edit_rect
                width: parent.width
                height: editing.paintedHeight
                color: "transparent"

                TextEdit {
                    id: editing

                    text: 'some text here'
                    font.family: 'Bitstream Vera Sans Mono'
                    font.pointSize: 14

                    Component.onCompleted: {
                        console.log('liveview is', liveview);
                        if (liveview) {
                            var corpus = [
        '',
        'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc condimentum ligula',
        'et massa ornare a feugiat nibh scelerisque. Aenean neque dolor, interdum sit amet',
        'nunc vel tortor auctor scelerisque. Suspendisse mi turpis, dapibus sit amet pulvinar sed, accumsan non est. Suspendisse varius',
        'sceler__ue__, pre__m ac purus. Sed nec augue sagittis velit molestie fringilla.',
        'Pellentesque aliquam nisi eget nunc bibendum fringilla.',
        '&*()_+-=~` dignissim volutpat',
        'justo, non consequat libero fermentum vel. Duis ornare egestas luctus. Fusce in',
        'nunc vel tortor auctor scelerisque. Suspendisse mi turpis, dapibus sit amet pulvinar sed, accumsan non__t. Suspendis',
        'quam quis nisi pelle[]{}\\|:;"\',.<>?/',
        'laoreet. In dignissim hendrerit ma!@#$%^vel sagittis. Integer fermentum vehicula',
        'nulla, in condimen__ nisi convallis et. Praesent condimentum turpis sit amet',
        'orci vehicula aliquet.',
        'Mauris accumsan scelerisque ligula, ut condimentum diam',
        'feugiat eu. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices',
        'posuere cubilia Curae\n'
                        ];

                            var lines = [];
                            for (var i = 0; i < 55; i++)
                                lines.push(corpus[Math.floor(Math.random() * corpus.length)]);
                            text = lines.join('\n');
                        }
                    }
                }
            }

            Rectangle {
                x: flick.contentX
                width: flick.width
                height: 20
                color: "#80aaaaff"

                Text {
                    anchors.fill: parent
                    horizontalAlignment: Text.AlignHCenter
                    text: "(end of file)"
                }
            }
        }
    }
}
