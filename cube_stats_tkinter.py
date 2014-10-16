#!/usr/bin/env python
import Tkinter as Tk
import matplotlib
from cube import MTG_Cube
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')

from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
# implement the default mpl key bindings
from matplotlib.backend_bases import key_press_handler


from matplotlib.figure import Figure

import sys

global cube

root = Tk.Tk()
root.wm_title("Cube Statistics")

def make_chart():
    global cube
    color = color_menu_value.get()
    cmc = cmc_menu_value.get()
    card_type = card_type_menu_value.get()
    factors = []
    if card_type != '':
        factors.append('Card_Type')
        factors.append(card_type)
    if color != '':
        factors.append('Color')
        factors.append(color)

    cmcs = cube.get_distinct('CMC', *factors)

    total_number = cube.get_number(*factors)
    y = []
    for cmc in cmcs:
        print 'CMC'
        print cmc
        filtered_number = cube.get_number('CMC',cmc,'Color', color)
        percent = filtered_number / total_number
        print filtered_number
        print percent
        y.append(percent)


    return cmcs,y

def update_graphs():
    f.clear()
    plot = f.add_subplot(111)
    x,y = make_chart()
    print x
    print y
    plot.bar(range(len(x)), y)
    plot.set_xticklabels(x)
    canvas.show()

f = Figure(figsize=(8,5), dpi=100)
a = f.add_subplot(111)

cube = MTG_Cube('cube')
plot = f.add_subplot(111)
factors = []
card_type = ''
color = 'MONO_RED'
if card_type != '':
    factors.append('Card_Type')
    factors.append(card_type)
if color != '':
    factors.append('Color')
    factors.append(color)

cmcs = cube.get_distinct('CMC', *factors)

total_number = cube.get_number(*factors)
y = []
for cmc in cmcs:
    print 'CMC'
    print cmc
    filtered_number = cube.get_number('CMC',cmc,'Color', color)
    percent = filtered_number / total_number
    print filtered_number
    print percent
    y.append(percent)
plot.bar(range(len(cmcs)), y)
plot.set_xticklabels(cmcs)

## Stealing from cube_statis
#plot = f.add_subplot(111, projection='3d')
#cube = MTG_Cube('cube')
#other_cube = MTG_Cube('cube_avg_360')
#colors = cube.get_distinct('Color')
#i = 1
#color_dic = {'MONO_BLACK':'k', 'MONO_BLUE':'b', 'MONO_GREEN':'g', 'MONO_WHITE':'w', 'MONO_RED':'r'}
#for color_id, color in enumerate(colors):
#    if "MONO_" not in color:
#        continue
#    i+= 1
#    print 'COLOR: {}'.format(color)

#    cmcs = cube.get_distinct('CMC', 'Color', color)
#    percents = []
#    for cmc_id, cmc in enumerate(cmcs):
#        print '    CMC: {}'.format(cmc)

#        color_total = cube.get_number('Color',color)
#        cmc_in_color = cube.get_number('CMC', cmc, 'Color', color)
#        percent = 100 * cmc_in_color / color_total
#        print '        My cube: {}/{}, {}%'.format(
#            cmc_in_color, color_total, percent)
#        percents.append(percent)
            
#        other_color_total = other_cube.get_number('Color',color)
#        other_cmc_in_color = other_cube.get_number('CMC', cmc, 'Color', color)
#        other_percent = 100 * other_cmc_in_color / other_color_total
#        print '        Other: {}/{}, {}%'.format(
#            other_cmc_in_color, other_color_total, other_percent)

#    print cmcs
#    print percents
#    #plot.bar(cmcs, percents, zs=color_id, zdir='y', color='r', alpha=.8)
#    plot.bar(cmcs, percents, zs=i, zdir='y', color=color_dic[color], alpha=.8)
#plot.set_xlabel('CMC')
#plot.set_zlabel('Percent')
#plot.set_ylabel('Color')
#color_labels = []
#for color in colors:
#    if "MONO_" in color:
#        color_labels.append('')
#plot.set_yticklabels(color_labels)
## end stealing

# a tk.DrawingArea
canvas = FigureCanvasTkAgg(f, master=root)
canvas.show()
#canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
canvas.get_tk_widget().grid(row=0,columnspan=5)

color_label = Tk.Label(root, text='Color')
color_menu_value = Tk.StringVar(root)
color_menu_value.set('')
color_menu = Tk.OptionMenu(root, color_menu_value, '', *cube.get_distinct('Color'))

color_label.grid(row=1, column=0)
color_menu.grid(row=2, column=0)

cmc_label = Tk.Label(root, text='Converted Mana Cost')
cmc_menu_value = Tk.StringVar(root)
cmc_menu_value.set('')
cmc_menu = Tk.OptionMenu(root, cmc_menu_value, '', *cube.get_distinct('CMC'))

cmc_label.grid(row=1, column=1)
cmc_menu.grid(row=2, column=1)

card_type_label = Tk.Label(root, text='Card Type')
card_type_menu_value = Tk.StringVar(root)
card_type_menu_value.set('')
card_type_menu = Tk.OptionMenu(root, card_type_menu_value, '', *cube.get_distinct('Card_Type'))

card_type_label.grid(row=1, column=2)
card_type_menu.grid(row=2, column=2)

update_button = Tk.Button(root, text="Update graphs", command=update_graphs)
update_button.grid(row=2, column=3)

Tk.mainloop()
# If you put root.destroy() here, it will cause an error if
# the window is closed with the window manager.