
from typing import List
from datetime import date

class Student:
    name: str
    group: str
    theme: str
    complex_mark: str
    prep: str
    #
    rating = 0.0
    theme_key: str
 
    def __init__(self, name: str, group: str, theme: str, complex_mark: int, prep: str):
        self.name = name
        self.group = group
        self.theme = theme
        self.complex_mark = complex_mark
        self.prep = prep

        pointIdx = self.theme.find('.')
        key = theme if pointIdx == -1 else theme[0:pointIdx]
        self.theme_key = key.replace('\n', '').replace('\r', '').lower().strip()

