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
            cmc_in_color = cube.get_number_within(cmc, 'Color', color)
            percent = 100 * cmc_in_color / color_total
            print '        My cube: {}/{}, {}%'.format(
                cmc_in_color, color_total, percent)
            
            other_color_total = other_cube.get_total_number(color)
            other_cmc_in_color = other_cube.get_number_within(cmc, 'Color', color)
            other_percent = 100 * other_cmc_in_color / other_color_total
            print '        Other: {}/{}, {}%'.format(
                other_cmc_in_color, other_color_total, other_percent)
            
def test():
    cube = MTG_Cube('cube')
    print cube.get_number_within('CMC', 'Color', 'MONO_RED')
    for x in cube.get_all_distinct('Color'):
        print x
    print cube.get_total_number('Color')
    print cube.get_distinct_within('CMC', 'Color', 'MONO_RED')
    
main()
