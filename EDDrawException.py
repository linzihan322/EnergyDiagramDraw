class EDDrawException(Exception):
    def __init__(self, error_type, message):
        self.error_type = error_type
        self.message = message

    def __str__(self):
        return f'{self.error_type}: {self.message}'


class EDDrawInternalException(EDDrawException):
    def __init__(self, message):
        super().__init__('InternalException', message)


class EDDrawParserException(EDDrawException):

    def __init__(self, error_type, source_line, message):
        super().__init__(error_type, message)
        self.source_line = source_line

    def __str__(self):
        return f'{self.error_type} at line {self.source_line}: {self.message}'


class EDDrawPreambleParserException(EDDrawParserException):
    def __init__(self, source_line, message):
        super().__init__('PreambleParserException', source_line, message)


class EDDrawDataParserException(EDDrawParserException):
    def __init__(self, source_line, message):
        super().__init__('DataParserException', source_line, message)


class EDDrawLabelParserException(EDDrawParserException):
    def __init__(self, source_line, message):
        super().__init__('LabelParserException', source_line, message)
