import copy
import inspect

from body.Logger import Logger
from intepreter.body.Preprocessor import Preprocessor
from intepreter.body.Validator import Validator
from intepreter.language.Semantic import Semantic
from intepreter.modules.DataProvider import DataProvider
from intepreter.modules.ModuleManager import ModuleManager
from intepreter.modules._interfaces.CommonLogic import CommonLogic
from intepreter.modules._interfaces.CommonValidator import CommonValidator


class Interpreter:
    def __init__(self):
        self.__validator = Validator()
        self.__preproccessor = Preprocessor()

    def parse_file(self, filename):
        filename = copy.deepcopy(filename)
        ModuleManager.download_default_modules()

        Logger.log("Compiling...")

        try:
            filename = self.__preproccessor.preprocess_file(filename)
        except Preprocessor.ParseException as exception:
            raise Interpreter.CompilationError("Compilation error: " + str(exception))

        Logger.log("Compilation succeed. Running...")

        with open(filename) as f:
            lines = [line.rstrip() for line in f]

        while True:
            idx = DataProvider.get_current_line()
            try:
                line = lines[idx]
            except IndexError:
                break

            if len(line) == 0:
                DataProvider.inc_current_line()
                continue

            try:
                self.__parse_line(line)
            except Interpreter.RunTimeError as exception:
                raise Interpreter.RunTimeError(
                    f"Runtime error. Line: {idx + 1}. " + str(exception)
                )

            DataProvider.inc_current_line()

        Logger.log("Program finished.")


    def __parse_line(self, line: str):
        parts = line.split()
        command, *params = parts

        self.__run_command(command, params)

    def __run_command(self, command, params):
        command = DataProvider.get_service_command(command)

        if ModuleManager.module_was_loaded('CORE'):
            for idx, param in enumerate(params):
                try:
                    CommonValidator.validate_name_variable(param)
                    CommonValidator.check_if_variable_exists(param)
                    variable = param[1:]
                    params[idx] = DataProvider.get_variable_value(variable)
                except Exception:
                    pass

        try:
            self.__validator.validate('command', (command.get_name(), params))
        except (Validator.ValidationError, CommonValidator.ValidationError) as exception:
            raise Interpreter.RunTimeError(f'Command: `{command.get_name()}`. ' +
                                           str(exception))

        param_types = command.get_param_types()
        for idx, param in enumerate(params):
            if inspect.isclass(param_types[idx]):
                params[idx] = param_types[idx](params[idx])
            else:
                break

        try:
            self.__validator.validate('command', (command.get_name(), params))
        except (Validator.ValidationError, CommonValidator.ValidationError) as exception:
            raise Interpreter.RunTimeError(f'Command: `{command.get_name()}`. ' +
                                           str(exception))

        if command.get_name() == Semantic.get_symbol('var'):
            new_command, *new_params = params[2:]
            self.__run_command(new_command, new_params)

            params = params[:2]
            params.append(DataProvider.get_returned_value())
            DataProvider.return_value(None)

        if command.get_name() == Semantic.get_symbol('import'):
            return

        try:
            command.get_exec_func()(*params)
        except CommonLogic.RunTimeError as exception:
            raise Interpreter.RunTimeError(
                f'Command: {command.get_name()}. '
                f'{str(exception)}'
            )

    #
    # Getters & Setters
    #

    class CompilationError(Exception):
        pass

    class RunTimeError(Exception):
        pass