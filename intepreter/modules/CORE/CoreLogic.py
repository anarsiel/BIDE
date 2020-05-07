from intepreter.modules.CORE.CoreValidator import CoreValidator
from intepreter.modules.DataProvider import DataProvider
from intepreter.modules._interfaces.CommonLogic import CommonLogic

class CoreLogic:
    @staticmethod
    def do_loop(cnt):
        DataProvider.append_values_stack(cnt)
        DataProvider.append_command_stack('loop')

    @staticmethod
    def do_endloop():
        DataProvider.set_peek_values_stack(DataProvider.peek_values_stack() - 1)
        if DataProvider.peek_values_stack() == 0:
            DataProvider.pop_command_stack()
            DataProvider.pop_values_stack()
            DataProvider.inc_current_line()  # stepping over loop's goto

    @staticmethod
    def do_goto(label):
        DataProvider.set_current_line(DataProvider.get_label_line(label))

    @staticmethod
    def do_label(label):
        DataProvider.set_label_line(label, DataProvider.get_current_line())

    @staticmethod
    def do_var(variable, separator, value):
        CommonLogic.set_variable(variable, value)

    @staticmethod
    def do_const(value):
        DataProvider.return_value(value)

class Core:
    __info = [
        ['import',  None, [str], None, None],
        ['endloop', CoreLogic.do_endloop, [], None, None],
        ['loop', CoreLogic.do_loop, [int], 'endloop', CoreValidator.validate_loop],
        ['goto', CoreLogic.do_goto, [str], None, CoreValidator.validate_goto],
        ['label', CoreLogic.do_label, [str], None, None],
        ['var', CoreLogic.do_var, [str, str, 'command'], None, CoreValidator.validate_var],
        ['const', CoreLogic.do_const, [str], None, None],
    ]

    @staticmethod
    def get_info():
        return Core.__info