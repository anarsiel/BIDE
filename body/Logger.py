class Logger:
    __console_message = "Console:\n"

    @classmethod
    def log(cls, message, end='\n'):
        cls.__console_message = cls.get_log() + message + end

    @classmethod
    def get_log(cls):
        if not cls.__console_message:
            return ""
        return cls.__console_message