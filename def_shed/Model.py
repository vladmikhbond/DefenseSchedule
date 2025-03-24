from typing import List, Set, Tuple
import pandas as pd
from .Student import Student
from .Team import Team
from .Slot import Slot
import random
from pathlib import Path
from datetime import date
from .Log import Log


class Model:
    """
    Модель отримує відносний шлях до вхідного excell-, наприклад, 'upload/Наказ.xlsx' зі вкладками Денне, ДЕК, Рейтинг, Бажання.

    Вихідний файл 'result.xlsx' створюєься в тому ж каталозі, наприклад, 'upload/result.xlsx'.
    """
    input_excell_file: str
    weights: Tuple[float, float]
    log: Log
    
    students: List[Student]
    teams: List[Team]
    slots: List[Slot]
     
    def __init__(self, input_excell_file, weights: Tuple[float, float]):
        self.weights = weights
        self.input_excell_file = input_excell_file
        self.log = Log(self.input_folder)
        try:
            self.students = self._load_order_sheet()
            self.slots = self._load_slots_sheet()
            self.teams = self._gather_teams()
            self._load_rating_sheet()

            self._distribution()
            self._excell_result()
        except BaseException as err:
            self.log.print(err.args)
                
    
    @property
    def input_folder(self):
        path = Path(self.input_excell_file)
        return path.parent


    @staticmethod 
    def fill_merged_cells(df, j):
        """ Заповнення пустот, що виникли внаслідок об'єднання клітинок """
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
        Model.fill_merged_cells(df, 1)
        self.log.print(f"Аркуш '{sheet}' \n ---")
        
        result = []
        for i in range(len(df)):
            if df.iloc[i, 2] == 0: 
                df.iloc[i, 2] = f'no theme {id(i)}'
                self.log.print(f"Відсутня тема. Керівник: {df.iloc[i, 1]} Студент: {df.iloc[i, 5]}, {df.iloc[i, 6]}")

            day = date(1,1,1) if df.iloc[i, 8] == 0 else df.iloc[i, 8].date()
            #    
            student = Student(
                name=df.iloc[i, 5], 
                group=df.iloc[i, 6], 
                theme=df.iloc[i, 2], 
                complex_mark=(int)(df.iloc[i, 4]), 
                prep=df.iloc[i, 1],
                desired_board_id= df.iloc[i, 7],   # if no wishes board_id = 0
                desired_day=day)
            
            result.append(student)
        
        return result
    
    def _load_slots_sheet(self) -> List[Student]:   
        sheet = 'ДЕК'
        df = pd.read_excel(self.input_excell_file, sheet)
        df = df.fillna(0)
        Model.fill_merged_cells(df, 0)
        # self.log.log(f"\nАркуш '{sheet}' \n ---")

        result = []
        for i in range(len(df)):
            slot = Slot(
                int(df.iloc[i, 0]), 
                df.iloc[i, 1].date(), 
                int(df.iloc[i, 2]))
            result.append(slot)
        
        return result

    def _load_rating_sheet(self):
        sheet = 'Рейтинг'
        df = pd.read_excel(self.input_excell_file, sheet)
        df = df.fillna(0)
        Model.fill_merged_cells(df, 0)
        self.log.print(f"\nАркуш '{sheet}' \n ---")

        for i in range(len(df)):
            group, name, rating = df.iloc[i, :]
            students = list(filter(lambda stud: stud.group == group and stud.name == name, self.students))
            if (len(students) == 1):  
                students[0].rating = rating
        # validation
        for st in self.students:
            if st.rating == 0:
                self.log.print(f"No rating. {st.name}, {st.group}")

  
    def _gather_teams(self) -> List[Team]:
        self.log.print(f"\nСтворення команд \n ---")
        set_of_keys: Set[str] = set()
        for student in self.students:
            set_of_keys.add(student.theme_key)

        # one theme_key is one team
        teams = []
        for key in set_of_keys:
            team_students = [s for s in self.students if s.theme_key == key]            
            team = Team(team_students)
            if len(team.students) > 0:
                teams.append(team)
                if team.desired[0] == date(1,1,1) or team.desired[1] == 0: 
                    self.log.print(f"Не обраний ДЕК чи дата захисту в команді: {key}")
            else:
                self.log.print(f"Пуста команда {key}")
        return teams


    def _distribution(self):
        """ single call only """
        self.log.print(f"\nDistribution' \n ---")
        
        self.teams.sort(key=lambda t: -t.rating)
        for team in self.teams:
            slot = self.find_nearest_slot(team)
            if slot:
                team.board_id = slot.board_id
                team.day = slot.day
                slot.teams.append(team)
            else:
                self.log.print(f"No accepteble slot for:\n{team}")
                team.day = date(1,1,1)

        
    def _excell_result(self):
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
        df_sorted.to_excel(f"{self.input_folder}/result.xlsx", index=False)


    def distance(self, team: Team, slot: Slot):
        b1, d1 = team.desired
        b2, d2 = slot.board_id, slot.day    

        return self.weights[0] * abs(b1 - b2) + self.weights[1] * abs((d1 - d2).days)

    def find_nearest_slot(self, team):
        free_slots = [s for s in self.slots if s.free_places >= len(team)]
        free_slots.sort(key=lambda slot: self.distance(team, slot))
        if len(free_slots): 
            return free_slots[0]
        return None
        

