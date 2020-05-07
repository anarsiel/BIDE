from intepreter.modules._interfaces.CommonValidator import CommonValidator


class AlgoValidator:
    @staticmethod
    def validate_inc(args):
        pass
        # try:
        #     int(args[0])
        # except:
        # CommonValidator.validate_name_variable(args[0])

    ""

    @staticmethod
    def validate_days_count_by_month(args):
        month = args[1]
        if month < 1 or month > 12:
            raise CommonValidator.ValidationError(
                f'Incorrect month: {month}'
            )

    @staticmethod
    def validate_get_month_name(args):
        month = args[0]
        if month < 1 or month > 12:
            raise CommonValidator.ValidationError(
                f'Incorrect month: {month}'
            )
