from selenium import webdriver

driver=webdriver.Chrome()
driver.get('https://www.fangraphs.com/leaders.aspx?pos=all&stats=rel&lg=all&qual=0&type=1&season=2019&month=1000&season1=2019&ind=0&team=0,ts&rost=0&age=0&filter=&players=0&startdate=2019-07-25&enddate=2019-07-31')
#driver.get('https://www.google.com/') #this replaces the open tab
csv_download = driver.find_element_by_id('LeaderBoard1_cmdCSV')
csv_download.click()
#TODO rename and move file to proper place
#TODO close browser after all links are downloaded

#current day
#https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=0&type=8&season=2019&month=1000&season1=2019&ind=0&team=0%2Cts&rost=0&age=0&filter=&players=0&startdate=2019-08-01&enddate=2019-08-01

#pitching 7 days
#https://www.fangraphs.com/leaders.aspx?pos=all&stats=rel&lg=all&qual=0&type=1&season=2019&month=1000&season1=2019&ind=0&team=0,ts&rost=0&age=0&filter=&players=0&startdate=2019-07-25&enddate=2019-07-31

#batting 7 days
#https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=0&type=1&season=2019&month=1000&season1=2019&ind=0&team=0,ts&rost=0&age=0&filter=&players=0&startdate=2019-07-25&enddate=2019-07-31

#defense 7 days
#https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=0&type=8&season=2019&month=1000&season1=2019&ind=0&team=0,ts&rost=0&age=0&filter=&players=0&startdate=2019-07-25&enddate=2019-07-31