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

    def fetchall(self):
        return [x[0] for x in self.cursor.fetchall()]

    def fetchone(self):
        return self.cursor.fetchone()[0]

    def get_all_distinct(self, table_name):
        table_name = '"' + table_name + '"' # Necessary to insert into SQLite statement
        self.cursor.execute("SELECT DISTINCT {} FROM Cards".format(table_name))
        return self.fetchall()

    def get_total_number(self, table_name):
        table_name = '"' + table_name + '"'
        self.cursor.execute("SELECT COUNT({}) AS Number FROM Cards WHERE {}=?", (table_name, table_name))
        return self.fetchone()

    def get_number_within(self, table_to_count, filter_table, filter_value):
        table_to_count = '"' + table_to_count + '"'
        filter_table = '"' + filter_table + '"'
        self.cursor.execute("SELECT COUNT({}) AS Number FROM Cards WHERE {}=?",
                            (table_to_count, filter_table, filter_value))
        return self.fetchall()
        
    def get_distinct_within(self, table_to_search, filter_table, filter_value):
        table_to_search = '"' + table_to_search + '"'
        filter_table = '"' + filter_table + '"'
        self.cursor.execute("SELECT DISTINCT {} FROM Cards WHERE {}=?",
                            (table_to_search, filter_table, filter_value))
        return self.fetchall()

    def get_number_within_two(self, table_to_count, filter_table_1, filter_value_1, filter_table_2, filter_value_2):
        table_to_count = '"' + table_to_count + '"'
        filter_table_1 = '"' + filter_table_1 + '"'
        filter_table_2 = '"' + filter_table_2 + '"'
        self.cursor.execute("SELECT COUNT({}) AS Number FROM Cards WHERE {}=? AND {}=?",
                            (table_to_count, filter_table_1, filter_value_1, filter_table_2, filter_value_2))
        return self.fetchall()

