"""produces static maps using mplleaflet which can be stitched together to produce a gif...vid???"""

import mplleaflet
import matplotlib.pyplot as plt
import numpy as np
import glob
from PIL import Image
from selenium import webdriver
import os

# create some dummy data
days_split = [2, 3, 5, 5, 7, 8, 9, 11, 14, 16, 8, 12, 6, 4]  # total should be length of lats/longs lists
days = []

for i in range(len(days_split)):
    days = days + [days_split.index(days_split[i])]*days_split[i]

lat_data = list(np.random.uniform(53.59, 53.51, 100))
long_data = list(np.random.uniform(-1.6, -1.4, 100))

alt_lat_data = list(np.random.uniform(53.59, 53.51, 100))
alt_long_data = list(np.random.uniform(-1.6, -1.4, 100))


# define some functions...
def lat_plot_data(i, input_list):

    subset_len = len([entry for entry in days if entry <= i])
    coord_list = input_list[0:subset_len]
    return coord_list


def long_plot_data(i, input_list):

    subset_len = len([entry for entry in days if entry <= i])
    coord_list = input_list[0:subset_len]
    return coord_list


for i in range(len(days_split)):

    lats = lat_plot_data(i, lat_data)
    longs = long_plot_data(i, long_data)

    alt_lats = lat_plot_data(i, alt_lat_data)
    alt_longs = long_plot_data(i, alt_long_data)

    plt.plot(longs, lats, 'rs')  # Draw red squares
    plt.plot(alt_longs, alt_lats, 'bs')  # Draw red squares

    mplleaflet.save_html(fileobj=str(i)+".html")
    # save as image


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
    area.save('00' + str(index), 'png')
    index += 1
