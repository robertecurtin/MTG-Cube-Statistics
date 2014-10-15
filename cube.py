import sqlite3
import csv

class MTG_Cube:
    def __init__(self, file_name):
        self.db = sqlite3.connect(':memory:')
        self.cursor = self.db.cursor()
        self.file_name = file_name
        
        self.cursor.execute('CREATE TABLE Cards (Card_Name text, Color text, Card_Type text, CMC integer, BLANK text)')
        self.db.commit()

        cube_file = open('{}.csv'.format(file_name),'rb')
        cube_reader = csv.reader(cube_file, delimiter=',', quotechar='"')
        self.cursor.executemany('INSERT INTO Cards VALUES (?,?,?,?,?)',cube_reader)
        cube_file.close()
        
        self.db.commit()

    def get_all_colors(self):
        self.cursor.execute("SELECT DISTINCT Color FROM Cards")
        value = [x[0] for x in self.cursor.fetchall()]
        return value

    def get_all_card_types(self):
        self.cursor.execute("SELECT DISTINCT Card_Type FROM Cards")
        value = [x[0] for x in self.cursor.fetchall()]
        return value
    
    def get_all_cmc(self):
        self.cursor.execute("SELECT DISTINCT CMC FROM Cards")
        value = [x[0] for x in self.cursor.fetchall()]
        return value
    
    def get_all_cmc_in_color(self, color):
        self.cursor.execute("SELECT DISTINCT CMC FROM Cards WHERE Color=?", (color,))
        value = [x[0] for x in self.cursor.fetchall()]
        return value
        
    def get_number_of_color(self, color):
        self.cursor.execute("SELECT COUNT(Color) AS Number FROM Cards WHERE Color=?", (color,))
        return self.cursor.fetchone()[0]

    def get_number_of_cmc_in_color(self, cmc, color):
        self.cursor.execute("SELECT COUNT(Color) AS Number FROM Cards WHERE CMC=? AND Color=?", (cmc,color))
        return self.cursor.fetchone()[0]
