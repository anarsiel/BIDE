from intepreter.language.Semantic import Semantic
from intepreter.modules.DataProvider import DataProvider
from intepreter.modules._interfaces.CommonValidator import CommonValidator


class CoreValidator:
    @staticmethod
    def validate_goto(args):
        if not args[0] in DataProvider.get_labels():
            raise CommonValidator.ValidationError(
                f"Wrong label name: `{args[0]}`."
            )

    @staticmethod
    def validate_loop(args):
        # if CommonValidator.looks_like_variable(args[0]):
        #     return
        #
        # args[0] = int(args[0])
        if args[0] <= 0:
            raise CommonValidator.ValidationError(
                f'Number of repetitions must be greater then zero. '
                f'You repeat {args[0]} times.'
            )

    @staticmethod
    def validate_var(args):
        if len(args) < 3:
            # this exception should never be raised
            # if command was validated successfully
            raise CommonValidator.ValidationError(
                f'Var command must have at least 3 args, not {len(args)}.'
            )

        CommonValidator.validate_name_variable('%' + args[0])

        if args[1] != Semantic.get_symbol('var_separator'):
            raise CommonValidator.ValidationError(
                f'Wrong var separator: `{args[1]}`. '
                f'You should use `{Semantic.get_symbol("var_separator")}`.'
            )