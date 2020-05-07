from intepreter.dynamic.Command import Command
from intepreter.modules.DataProvider import DataProvider


class CommonLogic:

    @staticmethod
    def set_variable(name : str, value):
        name = name.lstrip('%')
        DataProvider.set_variable_value(name, value)

    @staticmethod
    def get_variable(name: str):
        name = name.lstrip('%')
        return DataProvider.get_variable_value(name)

    @staticmethod
    def clear_variables():
        DataProvider.clear_variables()

    @staticmethod
    def add_command(name, function, attr_types, closing_command, validation):
        DataProvider.add_service_command(Command(name, function, attr_types, validation, closing_command))

    class RunTimeError(Exception):
        pass