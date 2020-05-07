from body.Logger import Logger


class IOLogic:
    @staticmethod
    def do_print_message(message):
        Logger.log(message)

    @staticmethod
    def print_to_file(filename, message):
        with open(filename, 'w') as f:
            f.write(message)


class IO:
    __info = [
        ['print', IOLogic.do_print_message, [str], None, None],
        ['print_to_file', IOLogic.print_to_file, [str, str], None, None],
    ]

    @staticmethod
    def get_info():
        return IO.__info
