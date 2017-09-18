from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import pandas as pd
from datetime import timedelta, date
from datetime import datetime
import numpy as np
import glob
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from selenium import webdriver
import os
import time
import mplleaflet

#reads in file
blackpool_df = pd.read_csv("BlackpoolMOD.csv")

#converts date to english format and a datetime format rather than string
blackpool_df['Date_of_Visit'] = pd.to_datetime(blackpool_df.Date_of_Visit, dayfirst = True)

#adds a column with day of year in it.
blackpool_df['Day_of_Year'] = blackpool_df.Date_of_Visit.dt.dayofyear

#reports the earliest day in the year of the sample.
minday = blackpool_df.Date_of_Visit.dt.dayofyear.min()

#takes the day in the year, minus the mininmum day of the year to return the number of day in the range
blackpool_df['Day_of_Range'] = blackpool_df.Day_of_Year - minday
#print (blackpool_df.head())



#makes a new df consisting of only those records that have no response
#nr_records = blackpool_df[blackpool_df.Visit_Outcome == 'No response']

#makes a df of only those with response
#r_records = blackpool_df[blackpool_df.Visit_Outcome == 'Response']

#produces longs and lats for responses and non responses
#rlon = r_records['LONGITUDE']
#rlat = r_records['LATITUDE']    
#nrlon = nr_records['LONGITUDE']
#nrlat = nr_records['LATITUDE']

#plots responses and non responses on a map.

#nr2_records = blackpool_df[(blackpool_df["Visit_Outcome"] == 'No response') & (blackpool_df["Day_of_Range"] == 2)]
#print (nr2_records)


for i in range(0,blackpool_df["Day_of_Range"].max()):
        
# (blackpool_df["Visit_Outcome"] == 'No response') & (blackpool_df["Day_of_Range"] <= 27)
        
        plt.plot(blackpool_df["LONGITUDE"],blackpool_df["LATITUDE"],'rs',markersize=2)
        
        r_records = blackpool_df[(blackpool_df["Visit_Outcome"] == 'Response') & (blackpool_df["Day_of_Range"] <= i)]
        
        
        plt.plot(r_records["LONGITUDE"],r_records["LATITUDE"],'gs',markersize=2)
        
     #   blackpool_df[(blackpool_df["Visit_Outcome"] == 'Response') & (blackpool_df["Day_of_Range"] <= i)]
        
      #  plt.plot(blackpool_df["LONGITUDE"],blackpool_df["LATITUDE"],'gs',markersize=2)
        
        mplleaflet.save_html(fileobj=str(i)+".html")
        
# get a list of all the files to open
glob_folder = os.path.join(os.getcwd(), '*.html')

html_file_list = glob.glob(glob_folder)




for html_file in html_file_list:

    # get the name into the right format
    temp_name = "file://" + html_file
    #print(len(temp_name))

    index = int(temp_name[31:-5])
    print(index)
    
    


    # open in webpage
    driver = webdriver.Chrome()
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


# define some functions...
def plot_data(i, input_list, list_length):

    subset_len = len([entry for entry in day if entry >= i])
    subset_pos = list_length - subset_len
    nr_coord_list = input_list[subset_pos:]
    coord_list = input_list[:subset_pos]
    return nr_coord_list, coord_list


for date in range(max(day)):

    nr_lats, lats = plot_data(date, lat, rs_list)
    nr_longs, longs = plot_data(date, long, rs_list)

    plt.plot(longs, lats, 'gs', markersize=1)  # Draws green squares
    plt.plot(nr_longs, nr_lats, 'rs', markersize=1)   # Draws red squares

    mplleaflet.save_html(fileobj=str(date)+".html")
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


