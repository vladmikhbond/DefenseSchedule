
from typing import List, Set
from datetime import date
from Slot import Slot
from Student import Student

class Team:
    students: List[Student] = []
    desired_day: date
    desired_board_id: int
    day: date
    board_id = 0

    @property
    def rating(self):
        """ Середній рейтинг членів команди """
        n = len(self.students)
        if n :
            return sum(student.rating for student in self.students) / n
        return 0

    @property
    def prep(self):
        return self.students[0].prep or 'nobody'
    
    def __str__(self):
        stud_names = ', '.join(s.name for s in self.students)
        desired = (self.desired_board_id, self.desired_day.strftime('%d.%m') )
        real = (self.board_id, self.day.strftime('%d.%m')) if self.board_id else 'n/a'
        return f"prep: {self.prep}  studs:{stud_names} \n rating: {self.rating:.2f} desired: {desired} real: {real} " 

    def __len__(self):
        return len(self.students)    
    
    @property
    def is_valid(self) -> bool:
        """ марки всіх студентів мають співпадати з кількістю студентів в команді"""
        n = len(self.students)
        if n == 1 and self.students[0].complex_mark <= 1:
            return True
        return all(s.complex_mark == n for s in self.students)
        
    
    def distance(self, slot:Slot):
        b1, d1 = self.desired_board_id, self.desired_day
        b2, d2 = slot.board_id, slot.day

        return abs(b1 - b2) * 10 + abs(d1.day_of_year - d2.day_of_year)

    def find_nearest_slot(self, slots: List[Slot]):
        accept_slots = [s for s in slots if s.free_places >= len(self)]
        accept_slots.sort(key=lambda s: self.distance(s))
        if len(accept_slots): 
            return accept_slots[0]
        return None
        
        
        

        