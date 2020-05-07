class Semantic:
    __extension = 'bpp'
    __variable_name_pattern = '[%][a-zA-Z_][a-zA-Z0-9_]*'
    __symbols = {'var_separator'   : ':=',
                 'var'             : 'var',
                 'import'          : 'import',
                 'return_variable' : '_'}

    __operators = [':=', '%']

    @staticmethod
    def get_variable_name_pattern():
        return Semantic.__variable_name_pattern

    @staticmethod
    def get_symbol(name):
        return Semantic.__symbols[name]

    @staticmethod
    def get_operators():
        return Semantic.__operators

    @staticmethod
    def get_extension():
        return Semantic.__extension