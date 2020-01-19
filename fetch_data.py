from selenium import webdriver
from selenium.webdriver.chrome.options import Options # remove popups
import shutil
import os.path
import time
from datetime import date, timedelta

DOWNLOAD_PATH = '../../../Downloads/FanGraphs Leaderboard.csv'
CURRENT_DAY_URL = 'https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=0&type=8&season=2019&month=1000&season1=2019&ind=0&team=0%2Cts&rost=0&age=0&filter=&players=0&startdate='
PITCHING_PAST_URL = 'https://www.fangraphs.com/leaders.aspx?pos=all&stats=rel&lg=all&qual=0&type=1&season=2019&month=1000&season1=2019&ind=0&team=0,ts&rost=0&age=0&filter=&players=0&startdate='
BATTING_PAST_URL = 'https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=0&type=1&season=2019&month=1000&season1=2019&ind=0&team=0,ts&rost=0&age=0&filter=&players=0&startdate='
FIELDING_PAST_URL = 'https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=0&type=8&season=2019&month=1000&season1=2019&ind=0&team=0,ts&rost=0&age=0&filter=&players=0&startdate='
sdate = date(2019, 3, 27)   # start date 3/27/2019 (+7 bc first week doesn't have data we want)
edate = date(2019, 9, 29)   # end date
delta = edate - sdate       # as timedelta


#init browser driver with pop-ups disabled
chrome_opts = Options()
chrome_opts.add_argument("--block-new-web-contents")
driver = webdriver.Chrome(options=chrome_opts)
#print(CURRENT_DAY_URL+curr_day+'&enddate='+curr_day)
    
#get all dates in season
for i in range(delta.days + 1):
    curr_day = sdate + timedelta(days=i)
    past_week_s = curr_day - timedelta(days=7)
    past_week_e = curr_day - timedelta(days=1)

    #cast to string
    curr_day = curr_day.strftime("%Y-%m-%d")
    past_week_s = past_week_s.strftime("%Y-%m-%d")
    past_week_e = past_week_e.strftime("%Y-%m-%d")
    #print(len(curr_day)) --> 10
    #print("Current day: " + curr_day + "\nWeek Start: "+ past_week_s + "\nWeek End: " + past_week_e + "\n")


    #current day
    driver.get(CURRENT_DAY_URL+curr_day+'&enddate='+curr_day)
    #driver.get('https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=0&type=8&season=2019&month=1000&season1=2019&ind=0&team=0%2Cts&rost=0&age=0&filter=&players=0&startdate=2019-08-01&enddate=2019-08-01')

    # #popup handling
    time.sleep(3)
    if driver.find_element_by_class_name('my_popup_close').is_displayed():
        popup_cancel = driver.find_element_by_class_name('my_popup_close')
        if popup_cancel.click():
            popup_cancel.click()
        time.sleep(3)
    csv_download = driver.find_element_by_id('LeaderBoard1_cmdCSV')
    csv_download.click()
    while not os.path.exists(DOWNLOAD_PATH):
        time.sleep(1)
    shutil.move(DOWNLOAD_PATH, './data/daily/'+curr_day+'.csv')
    print('Received ' + curr_day + ' data.')

    #pitching
    driver.get(PITCHING_PAST_URL+past_week_s+'&enddate='+past_week_e)
    #driver.get('https://www.fangraphs.com/leaders.aspx?pos=all&stats=rel&lg=all&qual=0&type=1&season=2019&month=1000&season1=2019&ind=0&team=0,ts&rost=0&age=0&filter=&players=0&startdate=2019-07-25&enddate=2019-07-31')
    #popup handling
    time.sleep(3)
    if driver.find_element_by_class_name('my_popup_close').is_displayed():
        popup_cancel = driver.find_element_by_class_name('my_popup_close')
        if popup_cancel.click():
            popup_cancel.click()
        time.sleep(3)
    csv_download = driver.find_element_by_id('LeaderBoard1_cmdCSV')
    csv_download.click()
    while not os.path.exists(DOWNLOAD_PATH):
        time.sleep(1)
    shutil.move(DOWNLOAD_PATH, './data/pitching/'+past_week_s+'_'+past_week_e+'.csv')
    print('Received pitching data from ' + past_week_s + ' to ' + past_week_e + '.')

    #batting
    driver.get(BATTING_PAST_URL+past_week_s+'&enddate='+past_week_e)
    #driver.get('https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=0&type=1&season=2019&month=1000&season1=2019&ind=0&team=0,ts&rost=0&age=0&filter=&players=0&startdate=2019-07-25&enddate=2019-07-31')
    #popup handling
    time.sleep(3)
    if driver.find_element_by_class_name('my_popup_close').is_displayed():
        popup_cancel = driver.find_element_by_class_name('my_popup_close')
        if popup_cancel.click():
            popup_cancel.click()
        time.sleep(3)
    csv_download = driver.find_element_by_id('LeaderBoard1_cmdCSV')
    csv_download.click()
    while not os.path.exists(DOWNLOAD_PATH):
        time.sleep(1)
    shutil.move(DOWNLOAD_PATH, './data/batting/'+past_week_s+'_'+past_week_e+'.csv')
    print('Received batting data from ' + past_week_s + ' to ' + past_week_e + '.')

    #fielding
    driver.get(FIELDING_PAST_URL+past_week_s+'&enddate='+past_week_e)
    #driver.get('https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=0&type=8&season=2019&month=1000&season1=2019&ind=0&team=0,ts&rost=0&age=0&filter=&players=0&startdate=2019-07-25&enddate=2019-07-31')
    #popup handling
    time.sleep(3)
    if driver.find_element_by_class_name('my_popup_close').is_displayed():
        popup_cancel = driver.find_element_by_class_name('my_popup_close')
        if popup_cancel.click():
            popup_cancel.click()
        time.sleep(3)
    csv_download = driver.find_element_by_id('LeaderBoard1_cmdCSV')
    csv_download.click()
    while not os.path.exists(DOWNLOAD_PATH):
        time.sleep(1)
    shutil.move(DOWNLOAD_PATH, './data/fielding/'+past_week_s+'_'+past_week_e+'.csv')
    print('Received fielding data from ' + past_week_s + ' to ' + past_week_e + '.')

driver.close()

#current day
#https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=0&type=8&season=2019&month=1000&season1=2019&ind=0&team=0%2Cts&rost=0&age=0&filter=&players=0&startdate=2019-08-01&enddate=2019-08-01

#pitching 7 days
#https://www.fangraphs.com/leaders.aspx?pos=all&stats=rel&lg=all&qual=0&type=1&season=2019&month=1000&season1=2019&ind=0&team=0,ts&rost=0&age=0&filter=&players=0&startdate=2019-07-25&enddate=2019-07-31

#batting 7 days
#https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=0&type=1&season=2019&month=1000&season1=2019&ind=0&team=0,ts&rost=0&age=0&filter=&players=0&startdate=2019-07-25&enddate=2019-07-31

#fielding 7 days
#https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=0&type=8&season=2019&month=1000&season1=2019&ind=0&team=0,ts&rost=0&age=0&filter=&players=0&startdate=2019-07-25&enddate=2019-07-31
