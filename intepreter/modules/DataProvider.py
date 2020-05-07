import copy

from intepreter.dynamic.Data import Data
from intepreter.dynamic.Command import Command
from intepreter.language.Semantic import Semantic


class DataProvider:
    @staticmethod
    def is_command(command: str):
        return command in Data.service_commands.keys()

    @staticmethod
    def is_opening_command(command: str):
        return command in Data.command_pairs.keys()

    @staticmethod
    def is_closing_command(command: str):
        return command in Data.command_pairs.values()

    @staticmethod
    def is_pair(command1: str, command2: str):
        return command1 is not None and \
               Data.command_pairs[command1] == command2

    #     
    #   Getters & Setters 
    # 

    @staticmethod
    def get_service_command(name) -> Command:
        return Data.service_commands[name]

    @staticmethod
    def add_service_command(command: Command):
        if command.get_closing_command():
            Data.command_pairs[
                command.get_name()] = command.get_closing_command()

        Data.service_commands[command.get_name()] = command

    ##################################

    @staticmethod
    def get_label_line(label):
        return Data.labels[label]

    @staticmethod
    def set_label_line(label, line):
        Data.labels[label] = line

    @staticmethod
    def get_labels():
        return Data.labels.keys()

    ##################################

    @staticmethod
    def get_variable_value(variable):
        return Data.variables[variable]

    @staticmethod
    def set_variable_value(variable, value):
        Data.variables[variable] = value

    @staticmethod
    def get_variables():
        return copy.deepcopy(Data.variables)

    @staticmethod
    def clear_variables():
        Data.variables.clear()

    ##################################

    @staticmethod
    def pop_command_stack():
        Data.command_stack.pop()

    @staticmethod
    def append_command_stack(value):
        Data.command_stack.append(value)

    @staticmethod
    def is_empty_command_stack():
        return len(Data.command_stack) == 0

    @staticmethod
    def get_command_stack():
        return copy.deepcopy(Data.command_stack)

    @staticmethod
    def clear_command_stack():
        Data.command_stack.clear()

    @staticmethod
    def peek_command_stack():
        try:
            return Data.command_stack[-1]
        except IndexError:
            return None

    ##################################

    @staticmethod
    def pop_values_stack():
        Data.values_stack.pop()

    @staticmethod
    def append_values_stack(value):
        Data.values_stack.append(value)

    @staticmethod
    def peek_values_stack():
        try:
            return Data.values_stack[-1]
        except IndexError:
            return None

    @staticmethod
    def set_peek_values_stack(value):
        try:
            Data.values_stack[-1] = value
        except IndexError:
            DataProvider.append_values_stack(value)

    ##################################

    @staticmethod
    def get_current_line():
        return Data.current_line

    @staticmethod
    def set_current_line(value):
        Data.current_line = value

    @staticmethod
    def inc_current_line():
        DataProvider.set_current_line(DataProvider.get_current_line() + 1)

    ##################################

    @staticmethod
    def get_returned_value():
        return DataProvider.get_variable_value(Semantic.get_symbol('return_variable'))

    @staticmethod
    def return_value(value):
        DataProvider.set_variable_value(Semantic.get_symbol('return_variable'),
                                        value)

    ##################################

    @staticmethod
    def get_service_commands_names():
        return Data.service_commands.keys()

    @staticmethod
    def get_function(command: str):
        return Data.service_commands[command].get_function()
    

    @staticmethod
    def get_arributes_count(command: str):
        return Data.service_commands[command].get_attr_count()

    #################################

    @staticmethod
    def reboot():
        Data.service_commands = {}
        Data.command_pairs = {}
        Data.labels = {}
        Data.variables = {}

        Data.command_stack = []
        Data.values_stack = []

        Data.current_line = 0
