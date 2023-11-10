import re
import string

SKIP = -9999


class DataSet:
    data = []
    labels = None
    count = 0
    max_energy = None
    min_energy = None
    delta_energy = None

    def set_data(self, input_line: string):
        self.data = []
        input_line = re.sub(r'\s+', '', input_line)
        splits = input_line.split(',')
        for s in splits:
            if s == '':
                self.data.append(SKIP)
            else:
                try:
                    value = float(s)
                except ValueError:
                    raise ValueError(f'''Invalid input '{s}'.''')
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
            raise Exception('''Missing labels.
--- Data and labels must be corresponding, even if the label is empty''')