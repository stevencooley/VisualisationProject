"""produces static maps using mplleaflet which can be stitched together to produce a gif...vid???"""

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import pandas as pd
from datetime import timedelta, date
from datetime import datetime
import datetime as dt
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

#nr2_records = blackpool_df[(blackpool_df["Visit_Outcome"] == 'No response') & (blackpool_df["Day_of_Range"] == 2)]
#print (nr2_records)


for i in range(0,blackpool_df["Day_of_Range"].max()+1):
        
# (blackpool_df["Visit_Outcome"] == 'No response') & (blackpool_df["Day_of_Range"] <= 27)
        
        plt.plot(blackpool_df["LONGITUDE"],blackpool_df["LATITUDE"],'rs',markersize=1)
        
        r_records = blackpool_df[(blackpool_df["Visit_Outcome"] == 'Response') & (blackpool_df["Day_of_Range"] <= i)]
                
        plt.plot(r_records["LONGITUDE"],r_records["LATITUDE"],'gs',markersize=1)
        
        
     #   blackpool_df[(blackpool_df["Visit_Outcome"] == 'Response') & (blackpool_df["Day_of_Range"] <= i)]
        
      #  plt.plot(blackpool_df["LONGITUDE"],blackpool_df["LATITUDE"],'gs',markersize=2)
        
        mplleaflet.save_html(fileobj=str(i)+".html")
        
# get a list of all the files to open
glob_folder = os.path.join(os.getcwd(), '*.html')

html_file_list = glob.glob(glob_folder)

start_date = dt.date(*map(int,"2017,4,13".split(',')))
print(start_date)


for html_file in html_file_list:

    # get the name into the right format
    temp_name = "file://" + html_file
    #print(len(temp_name))

    index = int(temp_name[31:-5])
    print(index)
    temp_date = start_date + dt.timedelta(days=index)
    
    


    # open in webpage
    driver = webdriver.Chrome()
    driver.get(temp_name)
    time.sleep(1.5)
    save_name = str(index) + '.png'
    driver.save_screenshot(save_name)
    driver.quit()

    img = Image.open(save_name)
    draw = ImageDraw.Draw(img)

    #fontPath = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    #font = ImageFont.truetype(fontPath, 32)
    draw.text((310, 110), "Day " + str(index) + ' '+str(temp_date), (0, 0, 0)) #,font=font)
    img.save(save_name)

    # crop as required
    box = (300, 100, 1000, 800)
    area = img.crop(box)

    if index >= 10:
        area.save('0' + str(index) + '.png')
    else:
        area.save('00' + str(index) + '.png')

