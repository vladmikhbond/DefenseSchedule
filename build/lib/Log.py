import random
import datetime

class Log:
    
    
    def __init__(self, folder: str):
        current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.path = f"{folder}/{current_time}.log"



    def print(self, message: str):
        with open(self.path, 'a') as f:
            print(message, file=f)


    