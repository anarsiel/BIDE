import re

from intepreter.language.Semantic import Semantic
from intepreter.modules.DataProvider import DataProvider


class CommonValidator:

    @staticmethod
    def validate_name_variable(value):
        value = str(value)
        if not bool(re.match(Semantic.get_variable_name_pattern(), value)):
            raise CommonValidator.ValidationError(
                f"Wrong variable name: {value[1:]}.")

    @staticmethod
    def check_if_variable_exists(value):
        value = value.lstrip('%')
        if value == Semantic.get_symbol('return_variable'):
            return

        if not value in DataProvider.get_variables().keys():
            raise CommonValidator.ValidationError(
                f"Variable do not exist: `{value}`.")

    @staticmethod
    def looks_like_variable(value):
        value = str(value)
        return len(value) > 0 and value[0] == '%'

    @staticmethod
    def validate_name_command(value):
        if not DataProvider.is_command(value):
            raise CommonValidator.ValidationError()

    class ValidationError(Exception):
        pass