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
        formatted = []
        for x in parameters:
            if (type(x) == str or type(x) == unicode): # Reformat strings, this is necessary to insert column titles into SQLite statements
                x = '"' + x + '"'
            else:
                print x
                print type(x)
            formatted.append(x)
        formatted = tuple(formatted)
        print command.format(*formatted)
        self.cursor.execute(command.format(*formatted))

    def get_distinct(self, column_to_search, *columninfo):
        command = "SELECT DISTINCT {} FROM Cards"
        if columninfo:
            command += " WHERE {}={}"
        for i in range(2, len(columninfo), 2):
            command += " AND {}={}"
        self.sql(command, column_to_search, *columninfo)
        return self.fetchall()

    def get_number(self, *columninfo): # Requires all tables to filter by in the format (table_name_1, filter_value_1, table_name_2, filter_value_2
        command = "SELECT COUNT(*) FROM Cards WHERE {0}={1}"
        for i in range(2, len(columninfo), 2):
            command += " AND {" + str(i) + "}={" + str(i+1) + "}"
        print command
        print columninfo
        self.sql(command, *columninfo)
        return float(self.fetchone())
