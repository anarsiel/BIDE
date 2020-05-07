from intepreter.body.Validator import Validator
from intepreter.language.Semantic import Semantic
from intepreter.modules.DataProvider import DataProvider
from intepreter.modules.ModuleManager import ModuleManager
from intepreter.modules._interfaces.CommonValidator import CommonValidator


class Preprocessor:
    def __init__(self):
        self.__command_to_func = {'loop' : self.__preprocess_loop,
                                  'endloop' : self.__preprocess_endloop}
        self.__validator = Validator()
        self.__label_count = 0

        self.__labels_stack = []

    def preprocess_file(self, filename):
        try:
            self.__validator.validate('filename', filename)
        except Validator.ValidationError as exception:
            raise Preprocessor.ParseException(str(exception))

        o_filename = filename.replace(f'.{Semantic.get_extension()}', f'.o.{Semantic.get_extension()}')
        with open(filename) as r:
            lines = [line.rstrip() for line in r]

            w = open(o_filename, 'w')

            for idx, line in enumerate(lines):
                try:
                    self.__preprocess_line(line, w)
                except Preprocessor.ParseException as exception:
                    raise Preprocessor.ParseException(f"Line: {idx + 1}. " +
                                                     str(exception))

            w.close()

        try:
            self.__validator.validate('command_stack', DataProvider.get_command_stack())
        except Validator.ValidationError as exception:
            raise Preprocessor.ParseException(str(exception))

        DataProvider.clear_command_stack()
        DataProvider.clear_variables()
        return o_filename

    def __preprocess_line(self, line, w):
        # comments
        line = line.split('#')[0]
        parts = line.strip().split()

        # no action in this string
        if len(parts) == 0:
            w.write('\n')
            return

        command, *params = parts

        if ModuleManager.module_was_loaded('CORE'):
            try:
                CommonValidator.check_if_variable_exists(command)

                leading_spaces = self.__get_leading_spaces(line)
                line = " ".join([' ' * leading_spaces, Semantic.get_symbol('var'), line.lstrip()])

                parts = line.strip().split()
                command, *params = parts
            except Exception as ignored:
                pass


        try:
            self.__validator.validate('command', (command, params))
        except Validator.ValidationError as exception:
            raise Preprocessor.ParseException(f"Command: `{command}`. " +
                                                str(exception))
        if command == Semantic.get_symbol('var'):
            DataProvider.set_variable_value(params[0], None)
        elif DataProvider.is_opening_command(command):
            DataProvider.append_command_stack(command)
        elif DataProvider.is_closing_command(command):
            DataProvider.pop_command_stack()

        try:
            self.__command_to_func[command](line, w)
        except KeyError:
            w.write(line + '\n')

    def __preprocess_loop(self, line, w):
        leading_spaces = len(line) - len(line.lstrip()) - 1
        leading_spaces = " " * leading_spaces

        w.write(leading_spaces + line + '\n')
        label = self.__gen_label()
        w.write(leading_spaces + 'label ' + label + '\n')
        self.__labels_stack.append(label)

    def __preprocess_endloop(self, line, w):
        leading_spaces = len(line) - len(line.lstrip()) - 1
        leading_spaces = " " * leading_spaces
        w.write(leading_spaces + line + '\n')
        w.write(leading_spaces + 'goto ' + self.__labels_stack[-1] + '\n')
        self.__labels_stack.pop()

    def __gen_label(self):
        label = "lbl" + str(self.__label_count)
        self.__label_count += 1
        return label

    def __get_leading_spaces(self, line):
        return len(line) - len(line.lstrip()) - 1

    class ParseException(Exception):
        pass