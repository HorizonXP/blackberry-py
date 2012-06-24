import bb.cascades 1.0

Page {
    id: root

    content: Container {
        layout: DockLayout {
        }

        background: Color.create("#ab8743")

        TextArea {
            text: "This way up \u2191 (size " + parent.width + "x" + parent.height + ")"
            editable: false
            backgroundVisible: false

            layoutProperties: DockLayoutProperties {
                horizontalAlignment: HorizontalAlignment.Fill
                verticalAlignment: VerticalAlignment.Center
            }
        }
    }
}
