"""produces static maps using mplleaflet which can be stitched together to produce a gif...vid???"""

import mplleaflet
import matplotlib.pyplot as plt
import numpy as np
import glob
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from selenium import webdriver
import os
import pandas as pd
import time

blackpool_df = pd.read_csv("BlackpoolMOD.csv")

# creating lists of data
lat = blackpool_df['LATITUDE'].tolist()
long = blackpool_df['LONGITUDE'].tolist()
response = blackpool_df['Day'].tolist()
rs_list = len(response)


# define some functions...
def plot_data(i, input_list, list_length):

    subset_len = len([entry for entry in response if entry >= i])
    subset_pos = list_length - subset_len
    nr_coord_list = input_list[subset_pos:]
    coord_list = input_list[:subset_pos]
    return nr_coord_list, coord_list


for day in range(max(response)):

    nr_lats, lats = plot_data(day, lat, rs_list)
    nr_longs, longs = plot_data(day, long, rs_list)

    plt.plot(longs, lats, 'gs', markersize=3)  # Draws green squares
    plt.plot(nr_longs, nr_lats, 'rs', markersize=3)   # Draws red squares


    """
    # First attempt to put in label - created world map
    fig = plt.figure()
    fig.suptitle('Day ' + str(response), fontsize=14, fontweight='bold')

    # Second attempt to put in label - created graph
    plt.title('Day ' + str(response))
    plt.show()
    """

    mplleaflet.save_html(fileobj=str(day)+".html")
    # saves as html file


# get a list of all the files to open
glob_folder = os.path.join(os.getcwd(), '*.html')

html_file_list = glob.glob(glob_folder)

for html_file in html_file_list:

    # get the name into the right format
    temp_name = "file://" + html_file

    index = int(temp_name[58:-5])

    # open in webpage
    driver = webdriver.Firefox()
    driver.get(temp_name)
    time.sleep(1.5)
    save_name = str(index) + '.png'
    driver.save_screenshot(save_name)
    driver.quit()

    img = Image.open(save_name)
    draw = ImageDraw.Draw(img)

    fontPath = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    font = ImageFont.truetype(fontPath, 32)
    draw.text((310, 110), "Day " + str(index), (0, 0, 0), font=font)
    img.save(save_name)

    # crop as required
    box = (300, 100, 1000, 800)
    area = img.crop(box)

    if index >= 10:
        area.save('0' + str(index), 'png')
    else:
        area.save('00' + str(index), 'png')



