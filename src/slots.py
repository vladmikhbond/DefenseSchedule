
from typing import List
from datetime import date
# from teams import Team

class Slot: 
    board_id: int
    day: date
    capacity: int
    teams: List = []

    def __init__(self, board_id: int, day: date, capacity: int):
        self.board_id = board_id
        self.day = day
        self.capacity = capacity
        self.teams = []

    def __str__(self):
        return f"{self.board_id}  {self.day}  {self.capacity}"
    
    @property
    def free_places(self):
        return self.capacity - sum( len(t) for t in self.teams)
    
    