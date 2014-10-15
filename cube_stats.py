import sqlite3
import csv
from cube import MTG_Cube

def main():
    personal_cube = MTG_Cube('cube')
    generic_360_cube = MTG_Cube('cube_avg_360')
    generic_720_cube = MTG_Cube('cube_avg_720')
    for color in personal_cube.get_all_colors():
        print 'COLOR: {}'.format(color)
        for cmc in personal_cube.get_all_cmc_in_color(color):
            print 'CMC: {}'.format(cmc)
            personal_number = personal_cube.get_number_of_color(color)
            personal_percent = 100 * personal_cube.get_number_of_cmc_in_color(cmc, color) / personal_number
            print 'Personal: {}, {}%'.format(personal_number, personal_percent)
            
            generic_360_number = generic_360_cube.get_number_of_color(color)
            generic_360_percent = 100 * generic_360_cube.get_number_of_cmc_in_color(cmc, color) / generic_360_number
            print 'Personal: {}, {}%'.format(generic_360_number, generic_360_percent)
            
            generic_720_number = generic_720_cube.get_number_of_color(color)
            generic_720_percent = 100 * generic_720_cube.get_number_of_cmc_in_color(cmc, color) / generic_720_number
            print 'Personal: {}, {}%'.format(generic_720_number, generic_720_percent)

def main2():
    db = sqlite3.connect(':memory:')
    cursor = db.cursor()

    print "Creating table"
    cursor.execute('CREATE TABLE cards_cube (Card_Name text, Color text, Card_Type text, CMC integer, BLANK text)')
    cursor.execute('CREATE TABLE cards_360 (Card_Name text, Color text, Card_Type text, CMC integer, BLANK text)')
    cursor.execute('CREATE TABLE cards_720 (Card_Name text, Color text, Card_Type text, CMC integer, BLANK text)')
    db.commit()

    print 'Opening file'

    cube_file = open('cube.csv','rb')
    cube_reader = csv.reader(cube_file, delimiter=',',quotechar='"')

    print 'Reading file'
    for line in cube_reader:
        cursor.execute('INSERT INTO cards_cube VALUES (?,?,?,?,?)',line)
    cube_file.close()
    
    db.commit()

    print 'Selecting black cards'
    #cursor.execute("SELECT COUNT(Color) AS NumberOfBlack FROM Cards WHERE Color='MONO_BLACK'")
    cursor.execute("SELECT DISTINCT Color FROM cards_cube")
    datas = cursor.fetchall()
    color_dictionary = {}
    for data in datas:
        cursor.execute("SELECT COUNT(Color) AS Number FROM cards_cube WHERE Color=?", data)
        number = cursor.fetchone()
        color_dictionary[data] = number[0]
        
    db.close()

main()
