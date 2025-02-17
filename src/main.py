from typing import List, Set
import scipy
import pandas as pd
from Student import Student
from Team import Team
from Slot import Slot
import random


def load_order_excell() -> List[Student]:
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
    df = pd.read_excel(path, sheet, engine="openpyxl")
   
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

def load_slots_excell() -> List[Student]:
    path = r'.\data\2024-2025_ПІ_Бакалаври.xlsx'
    sheet = 'Дні захисту'
    result = []
    df = pd.read_excel(path, sheet, engine="openpyxl")
    df = df.fillna(0)
    for i in range(len(df)):
        slot = Slot(
            int(df.iloc[i, 0]), 
            df.iloc[i, 1], 
            int(df.iloc[i, 2]))
        result.append(slot)
    return result


def get_raitings(students: List[Student]):
    """ stub """
    random.seed = 42
    for st in students:
        st.rating = random.uniform(0, 100)

def get_wishes(teams: List[Team], slots: List[Slot]):
    """ stub """
    random.seed = 42
    for t in teams:
        idx = random.randint(5, len(slots) - 1)
        t.desired_day = slots[idx].day
        t.desired_board_id = 1 if random.random() < 0.8 else 2

    
############### MAIN ###############

students = load_order_excell()
slots = load_slots_excell()
teams = Team.gather_teams(students)

get_raitings(students)
get_wishes(teams, slots)

# for s in students:
#     print(s.complex_mark, s.theme)
#     print(s.name, s.group, s.prep, s.rating, '\r\n')

for t in teams:
    # if not t.is_valid:
        print(t)

# for s in slots:
#     print(s)



