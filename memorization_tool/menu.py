from typing import Iterable


class Menu:
    def __init__(self):
        self._options = None  # dict of options

    @property
    def options(self):
        if self._options is None:
            raise ValueError('Options are not set')
        return self._options

    @options.setter
    def options(self, options: Iterable['Option']):
        self._options = {option.key: option for option in options}

    def print(self):
        for option in self.options:
            print(self.options[option].value)


class Option:
    def __init__(self, key: str, value: str, state):
        self.key = key
        self.value = value
        self.state = state
