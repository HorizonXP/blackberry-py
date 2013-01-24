import bb.cascades 1.0

Page {
    id: mainPage
    objectName: 'mainPage'

    Container {
        layout: DockLayout {}
        Container {
            horizontalAlignment: portrait ? HorizontalAlignment.Center : HorizontalAlignment.Left
            verticalAlignment: portrait ? VerticalAlignment.Top : VerticalAlignment.Center

            Label {
                multiline: true
                text: qsTr("Cascades LiveView")
                textStyle.fontSize: FontSize.PointValue
                textStyle.fontSizeValue: 16
            }

            Label {
                multiline: true
                text: "<html><p>Courtesy of the "
                    + "<a href='http://twitter.com/BBPyProject'>@BBPyProject</a>"
                    + "</p></html>"
                textStyle.fontSize: FontSize.PointValue
                textStyle.fontSizeValue: 10
            }
        }

        Container {
            background: Color.Gray

            horizontalAlignment: portrait ? HorizontalAlignment.Center : HorizontalAlignment.Right
            verticalAlignment: VerticalAlignment.Center

            preferredWidth: 650
            leftPadding: 30
            rightPadding: 30
            topPadding: 30
            bottomPadding: 30

            Label {
                multiline: true
                text: "<html><p>Select a .qml file in any folder as the LiveView target."
                    + " <b>The file must have a <span style='color:#d00000'>Page</span> as the top-level component</b>, "
                    + " and will be reloaded whenever you change it or any other .qml file"
                    + " in the same folder.</p></html>"
                textStyle.fontSize: FontSize.PercentageValue
                textStyle.fontSizeValue: 120
            }

            Button {
                horizontalAlignment: HorizontalAlignment.Center
                text: qsTr("Load QML")
                onClicked: {
                    filePicker.open();
                }
            }
        }

        Container {
            horizontalAlignment: portrait ? HorizontalAlignment.Center : HorizontalAlignment.Right
            verticalAlignment: VerticalAlignment.Bottom

            layout: StackLayout {
                orientation: LayoutOrientation.LeftToRight
            }

            Label {
                verticalAlignment: VerticalAlignment.Center
                text: qsTr("Keep-awake")
                textStyle.fontSize: FontSize.PercentageValue
                textStyle.fontSizeValue: 120
            }

            ToggleButton {
                verticalAlignment: VerticalAlignment.Center
                onCheckedChanged: {
                    keepAwake(checked);
                }
            }
        }
    }
}

