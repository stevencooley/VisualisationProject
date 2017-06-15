"""start of code to create animated graphics - in this case a bar plot"""


import matplotlib.pyplot as plt
from matplotlib import animation
import os
import pandas as pd

data_path = os.path.join(os.getcwd(), "new.csv")
results_data_df = pd.read_csv(data_path, index_col=0)
results_data_labels = results_data_df.index.values.tolist()
results_data = results_data_df.values.tolist()


def barlist(n):
    # need to return a list of values, so the row in the dataframe?
    return results_data[n]

fig = plt.figure()
fig.suptitle('start', fontsize=20)
plt.xlabel('Contact rates', fontsize=16)
plt.ylabel('% of total LSOAs', fontsize=16)


n = 6  # Number of frames
x = range(0, 100, 10)

barcollection = plt.bar(x, barlist(0), width=10)


def animate(i):  # i is what you cycle through (so rows or cols of a dataframe??)
    y = barlist(i)
    year = results_data_labels[i]
    fig.suptitle("LSOA contact rates for " + str(year), fontsize=16)
    for i, b in enumerate(barcollection):
        b.set_height(y[i])

anim = animation.FuncAnimation(fig, animate, repeat=True, blit=False, frames=n,
                               interval=1000)

anim.save('mymovie.mp4', writer=animation.FFMpegWriter(fps=1))
plt.show()
