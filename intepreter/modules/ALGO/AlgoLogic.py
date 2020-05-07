import calendar

from intepreter.modules.ALGO.AlgoValidator import AlgoValidator
from intepreter.modules.DataProvider import DataProvider


class AlgoLogic:
    @staticmethod
    def do_inc(value):
        DataProvider.return_value(value + 1)

    @staticmethod
    def do_concat(s, t):
        DataProvider.return_value(s + t)

    @staticmethod
    def do_replace(s, t1, t2):
        DataProvider.return_value(s.replace(t1, t2))

    @staticmethod
    def days_count_by_month(year, month):
        days = [31, 28 + (year % 4 == 0), 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        DataProvider.return_value(days[month - 1])

    @staticmethod
    def get_month_name(month):
        x = calendar.month_name[month]
        DataProvider.return_value(x)

    @staticmethod
    def format_length(string, length, symbol):
        res = symbol * (length - len(string)) + string
        DataProvider.return_value(res)

class Algo:
    __info = [
        ['inc', AlgoLogic.do_inc, [int], None, AlgoValidator.validate_inc],
        ['concat', AlgoLogic.do_concat, [str, str], None, None],
        ['replace', AlgoLogic.do_replace, [str, str, str], None, None],
        ['days_count_by_month', AlgoLogic.days_count_by_month, [int, int], None, AlgoValidator.validate_days_count_by_month],
        ['format_length', AlgoLogic.format_length, [str, int, str], None, None],
        ['get_month_name', AlgoLogic.get_month_name, [int], None, AlgoValidator.validate_get_month_name]
    ]

    @staticmethod
    def get_info():
        return Algo.__info
