"""produces static maps using mplleaflet which can be stitched together to produce a gif...vid???"""

import mplleaflet
import matplotlib.pyplot as plt
import numpy as np


days = [0, 0, 1, 1, 2, 2]
lat_data = list(np.random.uniform(53.59, 53.51, 100))
long_data = list(np.random.uniform(-1.6, -1.4, 100))
alt_lat_data = list(np.random.uniform(53.59, 53.51, 100))
alt_long_data = list(np.random.uniform(-1.6, -1.4, 100))

plt.plot(long_data, lat_data, 'rs')  # Draw red squares
plt.plot(alt_long_data, alt_lat_data, 'bs')  # Draw red squares

mplleaflet.show()