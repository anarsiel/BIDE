from imp import reload

from body.Indicators import Indicators
from body.Logger import Logger
from body.TextStyler import TextStyler
from intepreter.body.Interpreter import Interpreter
from intepreter.modules.DataProvider import DataProvider
from intepreter.modules.ModuleManager import ModuleManager


class Controller:
    __text = None
    __file_name = None

    @classmethod
    def run(cls):
        if not cls.__file_name:
            Logger.log("Before running, open some file")
            return

        cls.__reboot_core()

        interpreter = Interpreter()
        try:
            interpreter.parse_file(cls.__file_name)
        except (Interpreter.CompilationError, Interpreter.RunTimeError) as exception:
            Logger.log(str(exception))

    @classmethod
    def debug(cls):
        Logger.log('Debugger is not available yet')
        pass

    @classmethod
    def open_file(cls, path_to_file):
        Indicators.file_was_opened = True
        if path_to_file[0] != '/':
            cls.__file_name = "".join(["/", path_to_file])

        with open(cls.__file_name, 'r') as file:
            cls.__text = file.read()

        Logger.log(f'File opened: {path_to_file.split("/")[-1]}')

    @classmethod
    def save_file(cls, text):
        if not cls.__file_name:
            Logger.log("Before saving, open some file")
            return

        cls.__text = TextStyler.rich_2_plain(text)
        with open(cls.__file_name, 'w') as file:
            file.write(cls.__text)

        Logger.log(f'File saved: {cls.__file_name.split("/")[-1]}')

    #
    #   Getters
    #

    @classmethod
    def get_program_text(cls):
        Indicators.file_was_opened = False
        if not cls.__text:
            return ""

        return TextStyler.plain_2_rich(cls.__text)

    @classmethod
    def get_file_name(cls):
        if not cls.__file_name:
            return ""
        return cls.__file_name

    @classmethod
    def apply_style(cls, text):
        pure_text = TextStyler.rich_2_plain(text)
        return TextStyler.plain_2_rich(pure_text)

    @classmethod
    def file_was_opened(cls):
        return Indicators.file_was_opened

    @classmethod
    def is_text_empty(cls):
        return not cls.__text

    @classmethod
    def get_log(cls):
        return Logger.get_log()

    @classmethod
    def __reboot_core(cls):
        DataProvider.reboot()
        ModuleManager.reboot()

