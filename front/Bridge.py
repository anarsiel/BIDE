from PySide2.QtCore import Slot
from PySide2.QtQuickWidgets import QQuickWidget

from body.Controller import Controller


# noinspection PyCallingNonCallable
class Bridge(QQuickWidget):
    def __init__(self):
        super().__init__()

    #
    #   Slots
    #

    @Slot()
    def run(self):
        Controller.run()

    @Slot()
    def debug(self):
        Controller.debug()

    @Slot(str)
    def open_file(self, path_to_file):
        Controller.open_file(path_to_file)

    @Slot(str)
    def save_file(self, text):
        Controller.save_file(text)

    #
    #   Getters
    #

    @Slot(result=str)
    def get_program_text(self):
        return Controller.get_program_text()

    @Slot(result=str)
    def get_log(self):
        return Controller.get_log()

    @Slot(str, result=str)
    def get_program_text_styled(self, text):
        return Controller.apply_style(text)

    @Slot(result=bool)
    def was_file_opened(self):
        return Controller.file_was_opened()

    @Slot(result=bool)
    def is_text_empty(self):
        return Controller.is_text_empty()
