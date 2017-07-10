from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os
import numpy as np
import mplleaflet

# create some dummy data
days_split = [2, 3, 5, 5, 7, 8, 9, 11, 14, 16, 8, 12, 6, 4]  # total should be length of lats/longs lists
days = []

for i in range(len(days_split)):
    days = days + [days_split.index(days_split[i])]*days_split[i]

lat_data = list(np.random.uniform(53.59, 53.51, 100))
long_data = list(np.random.uniform(-1.6, -1.4, 100))

alt_lat_data = list(np.random.uniform(53.59, 53.51, 100))
alt_long_data = list(np.random.uniform(-1.6, -1.4, 100))

my_map = Basemap(resolution='f', # c, l, i, h, f or None
                 projection='merc',
                 lat_0=54.5, lon_0=-4.36,
                 llcrnrlon=-1.9, llcrnrlat=53.4, urcrnrlon=-1.2, urcrnrlat=53.7)

my_map.drawcoastlines()
my_map.drawcountries()
my_map.fillcontinents(color='#f2f2f2', lake_color='#46bcec')
my_map.drawmapboundary(fill_color='#46bcec')
my_map.drawmeridians(np.arange(0, 360, 30))
my_map.drawparallels(np.arange(-90, 90, 30))

shape_file_path = "map data"
file_name = "barnsley"
full_path = os.path.join(shape_file_path, file_name)
my_map.readshapefile(full_path, 'areas')

x, y = my_map(0, 0)
scatter = my_map.plot(x, y, 'bo')


def lat_plot_data(i, input_list):

    subset_len = len([entry for entry in days if entry <= i])
    coord_list = input_list[0:subset_len]
    return coord_list


def long_plot_data(i, input_list):

    subset_len = len([entry for entry in days if entry <= i])
    coord_list = input_list[0:subset_len]
    return coord_list


# animation function.  This is called sequentially
def animate(i):
    lats = lat_plot_data(i, lat_data)
    longs = long_plot_data(i, long_data)

    alt_lats = lat_plot_data(i, alt_lat_data)
    alt_longs = long_plot_data(i, alt_long_data)

    x1, y1 = my_map(longs, lats)
    x2, y2 = my_map(alt_longs, alt_lats)

    my_map.plot(x1, y1, '.', markersize='9', alpha=0.75, color='r')
    my_map.plot(x2, y2, '.', markersize='9', alpha=0.75, color='g')


# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(plt.gcf(), animate, frames=len(set(days)), interval=2000, blit=False, repeat=False)
#anim.save('barnsley_movie.mp4', writer=animation.FFMpegWriter(fps=1))

figManager = plt.get_current_fig_manager()
figManager.window.showMaximized()
plt.show()

