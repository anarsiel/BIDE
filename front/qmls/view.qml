import QtQuick 2.14
import QtQuick.Controls 2.14
import QtQuick.Layouts 1.11
import QtQuick.Dialogs 1.0

Rectangle {
    id: root
    width: 1100
    height: 800

    Rectangle {
        id: btns
        width: root.width
        height: root.height / 20
        color: "#808080"

        Rectangle {
            id: btns_rect
            width: parent.width
            height: parent.height
            anchors.verticalCenter: parent.verticalCenter

            color: '#808080'
            anchors.fill: parent
            anchors.leftMargin: 20
            anchors.rightMargin: 20

            Button {
                id: file_open_btn
                anchors.verticalCenter: parent.verticalCenter
                text: "open file"

                background: Rectangle {
                    radius: 2
                    implicitWidth: 100
                    implicitHeight: 24
                    border.color: "#333"
                    border.width: 1
                }

                onClicked: {
                    fileDialog.open();
                }

                FileDialog {
                    id: fileDialog
                    selectFolder: false
                    onAccepted: {
                        var path = this.fileUrl.toString();
                        // remove prefixed "file:///"
                        path = path.replace(/^(file:\/{3})/,"");
                        // unescape html codes like '%23' for '#'
                        var cleanPath = decodeURIComponent(path);
                        bridge.open_file(cleanPath)
                    }
                }
            }

            Button {
                id: save_btn
                text: "save"
                anchors.verticalCenter: parent.verticalCenter
                anchors.left : file_open_btn.right
                background: Rectangle {
                    radius: 2
                    implicitWidth: 100
                    implicitHeight: 24
                    border.color: "#333"
                    border.width: 1
                }

                onClicked: {
                    bridge.save_file(program_rect.text)
                }
            }
            Button {
                id: run_btn
                text: "run"
                anchors.verticalCenter: parent.verticalCenter
                anchors.right : debug_btn.left
                background: Rectangle {
                    radius: 2
                    implicitWidth: 100
                    implicitHeight: 24
                    border.color: "#333"
                    border.width: 1
                }

                onClicked: {
                    bridge.save_file(program_rect.text)
                    bridge.run()
                }
            }

            Button {
                id: debug_btn
                text: "debug"
                anchors.verticalCenter: parent.verticalCenter
                anchors.right : parent.right
                background: Rectangle {
                    radius: 2
                    implicitWidth: 100
                    implicitHeight: 24
                    border.color: "#333"
                    border.width: 1
                }

                onClicked: {
                    bridge.debug()
                }
            }
        }
    }

    Rectangle {
        id: upper_half
        width: root.width
        height: 4 * root.height / 5 - btns.height //- filename.height
        color: '#808080'
        anchors.top : btns.bottom
//        visible: false

        Rectangle {
            id: text_edit_rect
            width: parent.width
            height: parent.height

            color: '#E6E6FA'
            border.width: 1
            border.color: "black"
            anchors.fill: upper_half
            anchors.margins: 20

            ScrollView {
                id: scroll_view_edit
                anchors.fill: parent
                clip: true

                TextArea {
                    id: program_rect
                    anchors.fill: parent
                    padding: 20

                    textFormat : Text.RichText
                    focus : true

                    wrapMode: TextEdit.WordWrap

                    FpsTimer {
                        onTriggered: {

                            if (bridge.was_file_opened()) {
                                var cp = program_rect.cursorPosition
                                program_rect.text = bridge.get_program_text()
                                program_rect.cursorPosition = cp
                            }
                        }
                    }

                    FpsTimer {
                        interval: 5000;

                        onTriggered: {
                            if (!bridge.is_text_empty()) {
                                var cp = program_rect.cursorPosition
                                program_rect.text = bridge.get_program_text_styled(program_rect.text)
                                program_rect.cursorPosition = cp
                            }
                        }
                    }
                }
            }
        }
    }

    Rectangle {
        id: bottom_half
        width: root.width
        height: root.height - upper_half.height - btns.height
        anchors.top: upper_half.bottom
        anchors.left: upper_half.left
        color: "#808080"

        Rectangle {
            id: console_rect
            width: parent.width
            height: parent.height

            color: '#E6E6FA'
            border.width: 1
            border.color: "black"
            anchors.fill: bottom_half
            anchors.margins: 20
            anchors.topMargin: 0

            ScrollView {
                id: scroll_view_console
                anchors.fill: parent
                clip: true

                Text {
                    id: console_area
                    anchors.fill: parent
                    padding: 20

                    wrapMode: TextEdit.WordWrap

                    FpsTimer {
                        interval: 500;
                        onTriggered: {
                            console_area.text = bridge.get_log()
                        }
                    }
                }
            }
        }
    }
}