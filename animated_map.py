from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import os


lat_data = [53.8, 53.8, 53.8, 53.8]
long_data = [-1.54, -2, -2.2, -2.54]

my_map = Basemap(resolution='f', # c, l, i, h, f or None
                 projection='merc',
                 lat_0=54.5, lon_0=-4.36,
                 llcrnrlon=-6., llcrnrlat=49.5, urcrnrlon=2., urcrnrlat=55.2)

my_map.drawcoastlines()
my_map.drawcountries()
my_map.fillcontinents(color='#f2f2f2', lake_color='#46bcec')
my_map.drawmapboundary(fill_color='#46bcec')
my_map.drawmeridians(np.arange(0, 360, 30))
my_map.drawparallels(np.arange(-90, 90, 30))

shape_file_path = "map data"
file_name = "LA2013EW"
full_path = os.path.join(shape_file_path, file_name)
my_map.readshapefile(full_path, 'areas')

x, y = my_map(0, 0)
scatter = my_map.plot(x, y, 'bo')


def lat_plot_data(i):

    coord_list = lat_data[0:i+1]
    return coord_list


def long_plot_data(i):

    coord_list = long_data[0:i+1]
    return coord_list


# animation function.  This is called sequentially
def animate(i):
    lats = lat_plot_data(i)
    longs = long_plot_data(i)

    x, y = my_map(longs, lats)
    my_map.plot(x, y, 'bo')
    return scatter

# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(plt.gcf(), animate, frames=len(lat_data), interval=500, blit=False, repeat=True)

plt.show()
