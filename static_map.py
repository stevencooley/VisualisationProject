"""produces static maps using mplleaflet which can be stitched together to produce a gif...vid???"""

import mplleaflet
import matplotlib.pyplot as plt
import numpy as np
import glob
from PIL import Image
from selenium import webdriver
import os
import pandas as pd

blackpool_df = pd.read_csv("BlackpoolMOD.csv")

lat = blackpool_df['LATITUDE'].tolist()
long = blackpool_df['LONGITUDE'].tolist()
response = blackpool_df['Day'].tolist()



# define some functions...
def lat_plot_data(i, input_list):

    subset_len = len([entry for entry in response if entry <= i])
    coord_list = input_list[0:subset_len]
    return coord_list


def long_plot_data(i, input_list):

    subset_len = len([entry for entry in response if entry <= i])
    coord_list = input_list[0:subset_len]
    return coord_list


for day in range(1,28):

    lats = lat_plot_data(day, lat)
    longs = long_plot_data(day, long)

    plt.plot(longs, lats, 'rs')  # Draw red squares

    mplleaflet.save_html(fileobj=str(day)+".html")
    # save as image

"""

# get a list of all the files to open
glob_folder = os.path.join(os.getcwd(), '*.html')

html_file_list = glob.glob(glob_folder)
index = 1

for html_file in html_file_list:

    # get the name into the right format
    temp_name = "file://" + html_file

    # open in webpage
    driver = webdriver.Firefox()
    driver.get(temp_name)
    save_name = str(index) + '.png'
    driver.save_screenshot(save_name)
    driver.quit()

    # crop as required
    img = Image.open(save_name)
    box = (0, 0, 1440, 740)
    area = img.crop(box)

    if index >= 10:
        area.save('0' + str(index), 'png')
    else:
        area.save('00' + str(index), '.png')

    index += 1

"""

