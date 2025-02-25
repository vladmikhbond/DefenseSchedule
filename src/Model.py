from typing import List, Set, Tuple
import pandas as pd
from Student import Student
from Team import Team
from Slot import Slot
import random
from pathlib import Path

class Model:
    """
    Модель отримує відносний шлях до вхідного excell-, наприклад, 'upload/Наказ.xlsx' зі вкладками Денне, ДЕК, Рейтинг, Бажання.

    Вихідний файл 'result.xlsx' створюєься в тому ж каталозі, наприклад, 'upload/result.xlsx'.
    """

    input_excell_file: str
    weights: Tuple[float, float]

    students: List[Student]
    teams: List[Team]
    slots: List[Slot]
   
    def __init__(self, input_excell_file, weights: Tuple[float, float]):
        self.weights = weights
        self.input_excell_file = input_excell_file
        self.students = self._load_order_sheet()
        self.slots = self._load_board_sheet()
        self.teams = self._gather_teams()
        self._load_rating_sheet()
        self._add_wishes()

        self._distribution()

    
    
    @staticmethod 
    
    def fill_gaps(df, j):
        """ Заповнення пустот, що виникли псля об'єднання клітинок"""
        prev_val = 0
        for i in range(len(df)):        
            if df.iloc[i, j] == 0:
                df.iloc[i, j] = prev_val
            else:
                prev_val = df.iloc[i, j]

    def _load_order_sheet(self) -> List[Student]:
        """ Номери колонок:
        1 Керівник
        2 Тема
        4 Комплекс
        5 Студент
        6 Група
        """
        sheet = 'Денне'        
        df = pd.read_excel(self.input_excell_file, sheet)
        df = df.fillna(0)
        Model.fill_gaps(df, 1) 
        result = []
        for i in range(len(df)):
            if df.iloc[i, 2] == 0:
                df.iloc[i, 2] = f'no theme {id(i)}'
            student = Student(
                name=df.iloc[i, 5], 
                group=df.iloc[i, 6], 
                theme=df.iloc[i, 2], 
                complex_mark=(int)(df.iloc[i, 4]), 
                prep=df.iloc[i, 1]) 
            
            result.append(student)
        
        return result
    
    def _load_board_sheet(self) -> List[Student]:   
        sheet = 'ДЕК'
        df = pd.read_excel(self.input_excell_file, sheet)
        df = df.fillna(0)
        Model.fill_gaps(df, 0)
        
        result = []
        for i in range(len(df)):
            slot = Slot(
                int(df.iloc[i, 0]), 
                df.iloc[i, 1], 
                int(df.iloc[i, 2]))
            result.append(slot)
        return result

    def _load_rating_sheet(self):
        sheet = 'Рейтинг'
        df = pd.read_excel(self.input_excell_file, sheet)
        df = df.fillna(0)
        Model.fill_gaps(df, 0)

        for i in range(len(df)):
            group, name, rating = df.iloc[i, :]
            students = list(filter(lambda stud: stud.group == group and stud.name == name, self.students))
            if (len(students) == 1):  
                students[0].rating = rating
    


    def _add_wishes(self):
        """ stub """
        random.seed = 42
        bottom, top = 5, len(self.slots) - 1
        for t in self.teams:
            idx = random.randint(bottom, top)
            t.desired_day = self.slots[idx].day
            t.desired_board_id = 1 if random.random() < 0.8 else 2
            pass
  
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
            slot = self.find_nearest_slot(team)
            if slot:
                team.board_id = slot.board_id
                team.day = slot.day
                slot.teams.append(team)
            else:
                raise IndexError("No accepteble slots")
        
    def excell_result(self):
        df = pd.DataFrame([], columns=['ДЕК', 'Дата', 'Назва теми', 'Студент', 'Керівник'])
        i = 1
        for t in self.teams:
                for s in t.students:
                    df.loc[i] = [str(t.board_id), 
                        t.day.strftime('%d.%m'), 
                        s.theme.replace('\n', ' ').replace('\t', ' ').replace('\r', ''),
                        s.name, 
                        s.prep]
                    i += 1
        df_sorted = df.sort_values(by=[df.columns[0], df.columns[1]]) 
        
        # write down result 
        file_path = Path(self.input_excell_file)
        folder_path = file_path.parent
        df_sorted.to_excel(f"{folder_path}/result.xlsx", index=False)


    def distance(self, team: Team, slot: Slot):
        b1, d1 = team.desired_board_id, team.desired_day.day_of_year
        b2, d2 = slot.board_id, slot.day.day_of_year
        return self.weights[0] * abs(b1 - b2) + self.weights[1] * abs(d1 - d2)


    def find_nearest_slot(self, team):
        accept_slots = [s for s in self.slots if s.free_places >= len(team)]
        accept_slots.sort(key=lambda slot: self.distance(team, slot))
        if len(accept_slots): 
            return accept_slots[0]
        return None
        

