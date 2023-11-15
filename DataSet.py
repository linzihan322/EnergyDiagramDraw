import re
import string

from EDDrawException import EDDrawLabelParserException, EDDrawDataParserException

SKIP = -9999


class Settings:
    def __init__(self):
        self.decimal = 1
        self.number_font = 'normal'
        self.label_font = 'bold'
        self.color = (0, 0, 0)

    def __str__(self):
        return f'[decimal={self.decimal} numberfont={self.number_font} labelfont={self.label_font} color={self.color}]'


class DataSet:
    data = []
    labels = None
    count = 0
    max_energy = None
    min_energy = None
    delta_energy = None

    def __init__(self, source_line, settings=Settings()):
        self.source_line = source_line
        self.settings = settings

    def set_data(self, input_line: string):
        self.data = []
        input_line = re.sub(r'\s+', '', input_line)
        splits = input_line.split(',')
        for s in splits:
            if s == '':
                self.data.append(SKIP)
            else:
                try:
                    value = round(float(s), self.settings.decimal)
                except ValueError:
                    raise EDDrawDataParserException(self.source_line, f'''Invalid input '{s}'.
--- You can only input floating-point numbers in this line.''')
                if self.min_energy is None or self.min_energy > value:
                    self.min_energy = value
                if self.max_energy is None or self.max_energy < value:
                    self.max_energy = value
                self.delta_energy = self.max_energy - self.min_energy
                self.data.append(value)
        self.count = len(self.data)

    def set_labels(self, input_line: string):
        self.labels = []
        splits = input_line.split(',')
        for s in splits:
            self.labels.append(s.strip())
        if len(self.data) != len(self.labels):
            raise EDDrawLabelParserException(self.source_line, '''Missing labels.
--- Data and labels must be corresponding, even if the label is empty''')
