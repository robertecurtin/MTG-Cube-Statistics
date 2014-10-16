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

    def fetchall(self): # Returns a list of items from SQLite
        return [x[0] for x in self.cursor.fetchall()]

    def fetchone(self): # Fetches a single value from SQLite, such as the number returned by COUNT()
        return self.cursor.fetchone()[0]

    def sql(self, command, *parameters): # Runs the given command through SQLite, formatted with the given parameters
        parameters = tuple(['"' + str(x) + '"' for x in parameters]) # Necessary to insert into SQLite statement
        self.cursor.execute(command.format(*parameters))

    def get_all_distinct(self, column_name):
        self.sql("SELECT DISTINCT {} FROM Cards", column_name)
        return self.fetchall()

    def get_total_number(self, column_name):
        self.sql("SELECT COUNT({}) AS Number FROM Cards",column_name)
        return self.fetchone()

    def get_number_within(self, column_to_count, filter_column, filter_value):
        self.sql("SELECT COUNT({0}) AS Number FROM Cards WHERE {1}={2}",
                 column_to_count, filter_column, filter_value)
        return self.fetchone()
        
    def get_distinct_within(self, column_to_search, filter_column, filter_value):
        self.sql("SELECT DISTINCT {} FROM Cards WHERE {}={}",
                 column_to_search, filter_column, filter_value)
        return self.fetchall()

    def get_number_within_two(self, column_to_count, filter_column_1, filter_value_1, filter_column_2, filter_value_2):
        self.sql("SELECT COUNT({}) AS Number FROM Cards WHERE {}={} AND {}={}",
                 column_to_count, filter_column_1, filter_value_1, filter_column_2, filter_value_2)
        return self.fetchone()

