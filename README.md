I built a dataset of stats from the 2019 MLB baseball season using Python.

Stats were pulled from fangraphs.com using Selenium which is a web-based automation tool. Looking at the URL formats of fangraphs.com, I was able to automate switching between every day (and their respective previous week) in the database and clicking a download button to obtain the data in .csv format.

I also needed to find a schedule of 2019 MLB games in order to flip certain stats for the teams that were facing one another. This was obtained from https://newballpark.org/2018/08/25/2019-travel-grid-now-available/ I had to write another script to fill in this schedule with home games because it only contained the away games' schedule for any given team. 

After downloading all of the required data (749 files), it was all just a matter of parsing through the files and obtaining the information I desired. For every team on every day in the MLB schedule, I pulled that day's runs for the team, the team's past week's batting performance, their opponent's past week's bullpen performance, and their opponent's past week's defensive rating.

tl;dr
`fetch_data.py` uses Selenium to extract data from fangraphs.com
`fix_schedule.py` formats the schedule from https://newballpark.org/2018/08/25/2019-travel-grid-now-available/ to have home games as well as change the date format to remove the name of the day "MON, TUE, etc"
`pull.py` combines the files obtained from the above scripts into a single, clearly written .csv file with data for every team that was playing on every day in the 2019 MLB season.