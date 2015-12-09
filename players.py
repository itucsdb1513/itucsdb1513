import psycopg2 as dbapi2
from player import Player

class Players:
    def __init__(self):
        self.cp = cp
        return
    
    def get_playerslist(self):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            