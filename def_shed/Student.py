
from datetime import date

class Student:
    name: str
    group: str
    theme: str
    complex_mark: str
    prep: str
    desired_board_id: int
    desired_day: date
    
    #
    rating = 0.0
    theme_key: str
 
    def __init__(self, name: str, group: str, theme: str, complex_mark: int, prep: str, 
                 desired_board_id: int, desired_day: date):
        self.name = name
        self.group = group
        self.theme = theme
        self.complex_mark = complex_mark
        self.prep = prep
        self.desired_board_id = desired_board_id
        self.desired_day = desired_day

        pointIdx = self.theme.find('.')
        key = theme if pointIdx == -1 else theme[0:pointIdx]
        self.theme_key = key.replace('\n', '').replace('\r', '').lower().strip()

    def __str__(self):
        desired = (self.desired_board_id, self.desired_day.strftime('%d.%m') )
        return f"name: {self.name}  rating: {self.rating:.2f} desired: {desired}" 
