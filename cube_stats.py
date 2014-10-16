from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

from cube import MTG_Cube

def main():
    cube = MTG_Cube('cube')
    other_cube = MTG_Cube('cube_avg_360')
    level_1 = []
    other_level_1 = []
    level_2 = []
    other_level_2 = []
    
    fig = plt.figure()
    plot = fig.add_subplot(111, projection='3d')

    colors = cube.get_distinct('Color')
    i = 1
    for color_id, color in enumerate(colors):

        print 'COLOR: {}'.format(color)

        cmcs = cube.get_distinct('CMC', 'Color', color)
        percents = []
        for cmc_id, cmc in enumerate(cmcs):
            print '    CMC: {}'.format(cmc)

            color_total = cube.get_number('Color',color)
            cmc_in_color = cube.get_number('CMC', cmc, 'Color', color)
            percent = 100 * cmc_in_color / color_total
            print '        My cube: {}/{}, {}%'.format(
                cmc_in_color, color_total, percent)
            percents.append(percent)
            
            other_color_total = other_cube.get_number('Color',color)
            other_cmc_in_color = other_cube.get_number('CMC', cmc, 'Color', color)
            other_percent = 100 * other_cmc_in_color / other_color_total
            print '        Other: {}/{}, {}%'.format(
                other_cmc_in_color, other_color_total, other_percent)

        print cmcs
        print percents
        plot.bar(cmcs, percents, zs=color_id, zdir='y', color='r', alpha=.8)
    plot.set_xlabel('CMC')
    plot.set_zlabel('Percent')
    plot.set_ylabel('Color')
    plot.set_yticklabels(colors)

    plt.show()


            
def test():
    cube = MTG_Cube('cube')
    print cube.get_number_within('CMC', 'Color', 'MONO_RED')
    for x in cube.get_all_distinct('Color'):
        print x
    print cube.get_total_number('Color')
    print cube.get_distinct_within('CMC', 'Color', 'MONO_RED')
    

main()
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
for c, z in zip(['r', 'g', 'b', 'y'], [30, 20, 10, 0]):
    xs = np.arange(20)
    ys = np.random.rand(20)

    # You can provide either a single color or an array. To demonstrate this,
    # the first bar of each set will be colored cyan.
    cs = [c] * len(xs)
    cs[0] = 'c'
    ax.bar(xs, ys, zs=z, zdir='y', color=cs, alpha=0.8)

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

plt.show()

main()
