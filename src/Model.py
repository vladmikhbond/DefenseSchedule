from typing import List, Set, Tuple
import pandas as pd
from Student import Student
from Team import Team
from Slot import Slot
import random

class Model:
    students: List[Student]
    teams: List[Team]
    slots: List[Slot]
    
    def __init__(self):
        self.students = Model._load_order_excell()
        self.slots = Model._load_slots_excell()
        self.teams = self._gather_teams()
        self._add_raitings()
        self._add_wishes()

        self._distribution()
        


    @staticmethod    
    def _load_order_excell() -> List[Student]:
        """ Номери колонок:
        1 Керівник
        2 Тема
        4 Комплекс
        5 Студент
        6 Група
        [7 Рейтінг
        8 Номер ДЕКу
        9 Дата захисту]
        """
        path = r'.\data\2024-2025_ПІ_Бакалаври.xlsx'
        sheet = 'Денне'
        result = []
        df = pd.read_excel(path, sheet)  ##################
    
        df = df.fillna(0)
        prev_prep = 0
        for i in range(len(df)):
            prep = df.iloc[i, 1]        
            if prep == 0:
                prep = prev_prep
            else:
                prev_prep = prep
            if df.iloc[i, 2] == 0:
                df.iloc[i, 2] = f'no theme {id(i)}'
            student = Student(
                name=df.iloc[i, 5], 
                group=df.iloc[i, 6], 
                theme=df.iloc[i, 2], 
                complex_mark=(int)(df.iloc[i, 4]), 
                prep=prep) 
            
            result.append(student)
        
        return result
    
    @staticmethod
    def _load_slots_excell() -> List[Student]:
        path = r'.\data\2024-2025_ПІ_Бакалаври.xlsx'
        sheet = 'Дні захисту'
        result = []
        df = pd.read_excel(path, sheet)   ##################
        df = df.fillna(0)
        for i in range(len(df)):
            slot = Slot(
                int(df.iloc[i, 0]), 
                df.iloc[i, 1], 
                int(df.iloc[i, 2]))
            result.append(slot)
        return result

    def _add_raitings(self):
        """ stub """
        random.seed = 42
        for st in self.students:
            st.rating = random.uniform(0, 100)

    def _add_wishes(self):
        """ stub """
        random.seed = 42
        bottom, top = 5, len(self.slots) - 1
        for t in self.teams:
            idx = random.randint(bottom, top)
            t.desired_day = self.slots[idx].day
            t.desired_board_id = 1 if random.random() < 0.8 else 2

    
    def _gather_teams(self) -> List[Team]:
        theme_keys: Set[str] = set()
        for student in self.students:
            theme_keys.add(student.theme_key)

        teams = []
        for key in theme_keys:
            team = Team()
            team.students = [s for s in self.students if s.theme_key == key]
            teams.append(team)
        return teams


    def _distribution(self):
        """ single call only """
        self.teams.sort(key=lambda t: -t.rating)
        for team in self.teams:
            slot = team.find_nearest_slot(self.slots)
            if slot:
                team.board_id = slot.board_id
                team.day = slot.day
                slot.teams.append(team)
            else:
                raise IndexError("No accepteble slots")
        
    
    def csv_result(self):
        """ board, day, student, theme, prep """
        records: List[Tuple] = []
        for t in self.teams:
            for s in t.students:
                records.append((
                    str(t.board_id), 
                    t.day.strftime('%d.%m'), 
                    s.theme.replace('\n', ' ').replace('\t', ' ').replace('\r', ''), 
                    s.name, 
                    s.prep))
            
        records.sort()

        with open("data/res.csv", 'w') as f:
            for r in records:
                print('\t'.join(r), file=f)



