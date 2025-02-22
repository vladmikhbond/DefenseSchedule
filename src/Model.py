from typing import List, Set, Tuple
import pandas as pd
from Student import Student
from Team import Team
from Slot import Slot
import random
from pathlib import Path

# Модель отримує шлях до вхідного excell-файлу, наприклад 'upload/2024-2025_ПІ_Бакалаври.xlsx'.
# Вихідний файл 'result.xlsx' створюєься в тому ж каталозі, наприклад 'upload/result.xlsx'.
# 
class Model:

    input_excell_file: str
    students: List[Student]
    teams: List[Team]
    slots: List[Slot]
    input_excell_file: str

    def __init__(self, input_excell_file):
        self.input_excell_file = input_excell_file
        self.students = self._load_order_excell()
        self.slots = self._load_slots_excell()
        self.teams = self._gather_teams()
        self._add_raitings()
        self._add_wishes()

        self._distribution()
        
    
    def _load_order_excell(self) -> List[Student]:
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
        sheet = 'Денне'
        result = []
        df = pd.read_excel(self.input_excell_file, sheet)  ##################
    
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
    
    def _load_slots_excell(self) -> List[Student]:
        
        sheet = 'Дні захисту'
        result = []
        df = pd.read_excel(self.input_excell_file, sheet)  ##################
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



