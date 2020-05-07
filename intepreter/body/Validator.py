from os import path

from intepreter.language.Semantic import Semantic
from intepreter.modules.DataProvider import DataProvider
from intepreter.modules.ModuleManager import ModuleManager
from intepreter.modules._interfaces.CommonValidator import CommonValidator


class Validator:

    def __init__(self):
        self.__entity_to_func = {"filename" : self.__validate_filename,
                                 "command"  : self.__validate_command,
                                 "command_stack" : self.__validate_command_stack}

    #
    #   Public
    #

    def validate(self, type: str, value):
        if not type in self.__entity_to_func.keys():
            raise Validator.InvalidObjectTypeException(
                f"Wrong validation type: `{type}`."
            )

        try:
            self.__entity_to_func[type](value)
        except KeyError:
            DataProvider.get_service_command(type).get_validation_func()(value)
        except CommonValidator.ValidationError as exception:
            raise Validator.ValidationError(str(exception))

    #
    #   Private
    #

    def __validate_filename(self, value):
        if not path.isfile(value):
            raise Validator.ValidationError(
                f"File do not exist. "
                f"Check your filepath: `{value}`"
            )

        file_extension = value.split('.')[-1]
        if file_extension != 'rpaf':
            raise Validator.ValidationError(
                "File extension must be '.rpaf'."
            )

    @staticmethod
    def __validate_import(module):
        if not module in ModuleManager.get_registered_modules():
            raise Validator.ValidationError(
                f"Module doesn't exist: `{module}`"
            )
        pass

    @staticmethod
    def __import_module(module):
        ModuleManager.load_module(module)

    @staticmethod
    def __validate_command(value: (str, list)):
        command, params = value

        try:
            command = DataProvider.get_service_command(command)
        except KeyError:
            raise Validator.ValidationError(
                f"Wrong command name: `{command}`"
            )

        if command.get_name() != Semantic.get_symbol('var') and command.get_attr_count() != len(
                params):
            raise Validator.ValidationError(
                f"Wrong params count: found {len(params)}"
                f" instead of {command.get_attr_count()}"
            )

        if command.get_name() == Semantic.get_symbol('import'):
            Validator.__validate_import(params[0])
            Validator.__import_module(params[0])
            return

        param_types = command.get_param_types()
        for idx, param in enumerate(params):
            try:
                if ModuleManager.module_was_loaded('CORE'):
                    if CommonValidator.looks_like_variable(param):
                        raise ValueError

                param_types[idx](param)
            except ValueError:
                if ModuleManager.module_was_loaded('CORE'):
                    if CommonValidator.looks_like_variable(param):
                        CommonValidator.check_if_variable_exists(param)
                        continue

                raise Validator.ValidationError(
                    f"Wrong param type. Param #{idx + 1}: `{param}` "
                    f"cannot be casted to {param_types[idx]}. "
                )
            except TypeError:
                new_params = params[idx + 1:]
                Validator.__validate_command((param, new_params))
                break

        previous_command = DataProvider.peek_command_stack()
        if DataProvider.is_closing_command(command.get_name()) and \
                not DataProvider.is_pair(previous_command,
                                 command.get_name()):
            raise Validator.ValidationError(
                f"Wrong command pair: [{previous_command}, {command.get_name()}]."
            )

        try:
            command.get_validation_func()(params)
        except TypeError as ignored:
            # some commands may have no validation function
            pass


    def __validate_command_stack(self, c_stack : list):
        if len(c_stack) > 0:
            raise Validator.ValidationError(
                f'Commands: {str(c_stack)} - have no pair'
            )


    #
    #   Exceptions
    #

    class InvalidObjectTypeException(Exception):
        pass

    class ValidationError(Exception):
        pass