import sqlite3
import csv
from cube import MTG_Cube

def main():
    cube = MTG_Cube('cube')
    other_cube = MTG_Cube('cube_avg_360')
    level_1 = []
    other_level_1 = []
    level_2 = []
    other_level_2 = []
    
    for color in cube.get_all_distinct('Color'):
        print 'COLOR: {}'.format(color)

        for cmc in cube.get_distinct_within('CMC', 'Color', color):

            print '    CMC: {}'.format(cmc)

            color_total = cube.get_total_number(color)
            cmc_in_color = cube.get_number_within(cmc, color)
            percent = 100 * cmc_in_color / color_total
            print '        My cube: {}/{}, {}%'.format(
                cmc_in_color, color_total, percent)
            
            other_color_total = other_cube.get_total_number(color)
            other_cmc_in_color = other_cube.get_number_within(cmc, color)
            other_percent = 100 * other_cmc_in_color / other_color_total
            print '        Other: {}/{}, {}%'.format(
                other_cmc_in_color, other_color_total, other_percent)
            

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
