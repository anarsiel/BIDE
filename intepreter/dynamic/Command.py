class Command:
    def __init__(self, name, function, attr_types, validation, closing_command):
        self.__name = name
        self.__function = function
        self.__attr_types = attr_types
        self.__validation = validation
        self.__closing_command = closing_command

    def get_name(self):
        return self.__name

    def get_exec_func(self):
        return self.__function

    def get_attr_count(self):
        return len(self.__attr_types)

    def get_param_types(self):
        return self.__attr_types

    def get_validation_func(self):
        return self.__validation

    def get_closing_command(self):
        return self.__closing_command