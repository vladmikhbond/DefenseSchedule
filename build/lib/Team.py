
from typing import List, Set
from datetime import date
from Slot import Slot
from Student import Student

class Team:
    students: List[Student] = []
    day = date(1,1,1)
    board_id = 0
    rating: int   # Середній рейтинг членів команди
    
    def __init__(self, students: List[Student]):
        self.students = students
        self.rating = sum(st.rating for st in students) / len(students)
        day = max(st.desired_day for st in students)
        id = max(st.desired_board_id for st in students)
        self.desired = (day, id)
        

    @property
    def prep(self):
        return self.students[0].prep or 'nobody'    
    
    def __str__(self):
        stud_names = ', '.join(s.name for s in self.students)
        
        real = (self.board_id, self.day.strftime('%d.%m')) if self.board_id else 'n/a'
        return f"prep: {self.prep}  studs:{stud_names} \n rating: {self.rating:.2f} desired: {self.desired} real: {real} " 

    def __len__(self):
        return len(self.students)    
    
    @property
    def is_valid(self) -> bool:
        """ марки всіх студентів мають співпадати з кількістю студентів в команді"""
        n = len(self.students)
        if n == 1 and self.students[0].complex_mark <= 1:
            return True
        return all(s.complex_mark == n for s in self.students)


        