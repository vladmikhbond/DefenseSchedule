
from typing import List, Set
from datetime import date
from Student import Student

class Team:
    students: List[Student] = []
    desired_day: date
    desired_board_id: int
    day: date
    board_id: int

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
        studs = ', '.join(s.name for s in self.students)
        return f"{self.prep}:  {studs}  {self.desired_board_id} {self.desired_day}"
    
    @property
    def is_valid(self) -> bool:
        """ марки всіх студентів мають співпадати з кількістю студентів в команді"""
        n = len(self.students)
        if n == 1 and self.students[0].complex_mark <= 1:
            return True
        return all(s.complex_mark == n for s in self.students)
        

        
    @staticmethod
    def gather_teams(students: List[Student]) -> List:
        theme_keys: Set[str] = set()
        for student in students:
            theme_keys.add(student.theme_key)

        teams = []
        for key in theme_keys:
            team = Team()
            team.students = [s for s in students if s.theme_key == key]
            teams.append(team)
        return teams
