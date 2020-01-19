import csv
from datetime import date, timedelta
# https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=0&type=8&season=2019&month=0&season1=2019&ind=0&team=0,ts&rost=0&age=0&filter=&players=0&startdate=&enddate=

#dict to get team abbreviations from full names retrieved from stat spreadsheets
team_abbs = {'Diamondbacks': 'ARI',
            'Braves': 'ATL',
            'Orioles': 'BAL',
            'Red Sox': 'BOS',
            'Cubs': 'CHC',
            'White Sox': 'CWS',
            'Reds': 'CIN',
            'Indians': 'CLE',
            'Rockies': 'COL',
            'Tigers': 'DET',
            'Marlins': 'MIA',
            'Astros': 'HOU',
            'Royals': 'KC',
            'Angels': 'LAA',
            'Dodgers': 'LAD',
            'Brewers': 'MIL',
            'Twins': 'MIN',
            'Mets': 'NYM',
            'Yankees': 'NYY',
            'Athletics': 'OAK',
            'Phillies': 'PHI',
            'Pirates': 'PIT',
            'Padres': 'SD',
            'Giants': 'SF',
            'Mariners': 'SEA',
            'Cardinals': 'STL',
            'Rays': 'TB',
            'Rangers': 'TEX',
            'Blue Jays': 'TOR',
            'Nationals': 'WAS'
}
#dict to get team abbreviations from indices of my schedule file
team_col_rev = {
    1:'SEA',
    2:'SF',
    3:'OAK',
    4:'LAD',
    5:'LAA',
    6:'SD',
    7:'ARI',
    8:'COL',
    9:'TEX',
    10:'HOU',
    11:'KC',
    12:'STL',
    13:'MIN',
    14:'MIL',
    15:'CHC',
    16:'CWS',
    17:'DET',
    18:'CLE',
    19:'CIN',
    20:'PIT',
    21:'TOR',
    22:'BOS',
    23:'NYY',
    24:'NYM',
    25:'PHI',
    26:'BAL',
    27:'WAS',
    28:'ATL',
    29:'TB',
    30:'MIA',
}

def main():
    sched = getSchedule()
    sdate = date(2019, 4, 4)   # start date 4/4/2019 because we want a full week of data
    edate = date(2019, 9, 29)   # end date
    delta = edate - sdate       # as timedelta

    for i in range(delta.days + 1):
        curr_day = sdate + timedelta(days=i)
        past_week_s = curr_day - timedelta(days=7)
        past_week_e = curr_day - timedelta(days=1)

        #cast dates to strings, special formatting to match schedule file
        curr_day_sched_format = curr_day.strftime("%m/%d/%Y")
        curr_day_sched_format = curr_day_sched_format[0:6]+curr_day_sched_format[8:] # remove '20' from '2019'

        temp_start = past_week_s.strftime("%m/%d/%Y")
        temp_start = temp_start[0:6]+temp_start[8:] # remove '20' from '2019'
        temp_end = past_week_e.strftime("%m/%d/%Y")
        temp_end = temp_end[0:6]+temp_end[8:] # remove '20' from '2019'
        past_week_sched_format = temp_start + '-' + temp_end
        

        curr_day_file = curr_day.strftime("%Y-%m-%d")+'.csv'
        past_week_s = past_week_s.strftime("%Y-%m-%d")
        past_week_e = past_week_e.strftime("%Y-%m-%d")
        past_week_file = past_week_s+'_'+past_week_e+'.csv'
        
        print("Working on current day: " + curr_day_sched_format)
        extractDay(curr_day_file, past_week_file, sched, curr_day_sched_format, past_week_sched_format)

#utility function that converts percentage strings to floats
def p2f(x):
    return round(float(x.strip('%'))/100, 3)

#extract schedule data
def getSchedule():
    schedule = {} #schedule format ==> {date1: {team1:team2, ...}, date2: {...}, ...}
    with open('data/2019_matchups_fixed.csv') as sched_file:
        sched_reader = csv.reader(sched_file, delimiter=',')
        
        line_count = 0
        for row in sched_reader:
            if line_count == 0:
                #print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                games = {}
                for i in range(1,len(row)):
                    if row[i] != '' and row[i] != 'All Star Game':
                        games[row[i]] = team_col_rev[i]
                schedule[row[0]] = games
    return schedule

#write data for one day
# curr_day and past_week are the .csv filenames located in ./data/
def extractDay(curr_day, past_week, schedule, curr_day_sched_format, past_week_sched_format):
    teams_data = {}
    #read current day runs
    with open('data/daily/'+curr_day) as cd_file:
        cd_reader = csv.reader(cd_file, delimiter=',')
        
        line_count = 0
        for row in cd_reader:
            if line_count == 0:
                #print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                #teams_data += [[row[0], row[4]]]
                teams_data[team_abbs[row[0]]] = {'runs': row[4]} #NOTE it's not safe to hard code row indices such as row[0]

    #read past 7 days batting stats
    with open('data/batting/'+past_week) as bat_file:
        bat_reader = csv.reader(bat_file, delimiter=',')
        
        line_count = 0
        for row in bat_reader:
            if line_count == 0:
                #print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                #we only want past-data for the teams playing on the current day
                team = team_abbs[row[0]]
                if team in teams_data:
                    teams_data[team]['BB%'] = p2f(row[2]) # NOTE some error occurs with batting in first week
                    teams_data[team]['K%'] = p2f(row[3])
                    teams_data[team]['ISO'] = row[9]
                    teams_data[team]['BABIP_BAT'] = row[11]
                    teams_data[team]['wOBA'] = row[17]
                    teams_data[team]['wRAA'] = row[16]

    #read past 7 days bullpen stats
    with open('data/pitching/'+past_week) as pitch_file:
        pitch_reader = csv.reader(pitch_file, delimiter=',')
        rows = list(pitch_reader) # have to store into list because im using it twice

        #get data of current team temporarily without flipping with opponent stats
        non_reversed_pitch = {}
        line_count = 0
        for row in rows:
            if line_count == 0:
                #print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                #we only want past-data for the teams playing on the current day
                team = team_abbs[row[0]]
                if team in teams_data:
                    #get data of team without flipping stats
                    non_reversed_pitch[team] = {}
                    non_reversed_pitch[team]['WHIP'] = row[9]
                    non_reversed_pitch[team]['BABIP_PITCH'] = row[10]
                    non_reversed_pitch[team]['LOB%'] = p2f(row[11])
                    non_reversed_pitch[team]['FIP-'] = row[13]
                    non_reversed_pitch[team]['xFIP-'] = row[14]
                    non_reversed_pitch[team]['SIERA'] = row[19]
                    
        #get opponent data into team_data data structure (which we care about)
        line_count = 0
        for row in rows:
            if line_count == 0:
                #print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                #we only want past-data for the teams playing on the current day
                team = team_abbs[row[0]]
                if team in teams_data:
                    #find current team's daily opponent
                    if team in schedule[curr_day_sched_format]:
                        oppo = schedule[curr_day_sched_format][team] #TODO add in error case if not found
                        if oppo in non_reversed_pitch:
                            teams_data[team]['WHIP'] = non_reversed_pitch[oppo]['WHIP']
                            teams_data[team]['BABIP_PITCH'] = non_reversed_pitch[oppo]['BABIP_PITCH']
                            teams_data[team]['LOB%'] = non_reversed_pitch[oppo]['LOB%']
                            teams_data[team]['FIP-'] = non_reversed_pitch[oppo]['FIP-']
                            teams_data[team]['xFIP-'] = non_reversed_pitch[oppo]['xFIP-']
                            teams_data[team]['SIERA'] = non_reversed_pitch[oppo]['SIERA']
                        else: # this happens when opposing team does not have past data (i.e first week or all star break(?))
                            teams_data[team]['WHIP'] = ''
                            teams_data[team]['BABIP_PITCH'] = ''
                            teams_data[team]['LOB%'] = ''
                            teams_data[team]['FIP-'] = ''
                            teams_data[team]['xFIP-'] = ''
                            teams_data[team]['SIERA'] = ''
                    else:
                        teams_data[team]['WHIP'] = 'UNSCHEDULED GAME'
                        teams_data[team]['BABIP_PITCH'] = 'UNSCHEDULED GAME'
                        teams_data[team]['LOB%'] = 'UNSCHEDULED GAME'
                        teams_data[team]['FIP-'] = 'UNSCHEDULED GAME'
                        teams_data[team]['xFIP-'] = 'UNSCHEDULED GAME'
                        teams_data[team]['SIERA'] = 'UNSCHEDULED GAME'


    #read past 7 days defense stats
    with open('data/fielding/'+past_week) as def_file:
        def_reader = csv.reader(def_file, delimiter=',')
        rows = list(def_reader) # have to store into list because im using it twice

        #get data of current team temporarily without flipping with opponent stats
        non_reversed_def = {}
        line_count = 0
        for row in rows:
            if line_count == 0:
                #print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                #we only want past-data for the teams playing on the current day
                team = team_abbs[row[0]]
                if team in teams_data:
                    #get data of team without flipping stats
                    non_reversed_def[team] = {}
                    non_reversed_def[team]['DEF'] = row[18]

                    
        #get opponent data into team_data data structure (which we care about)
        #pitch_reader_2 = csv.reader(pitch_file, delimiter=',')
        line_count = 0
        for row in rows:
            if line_count == 0:
                #print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                #we only want past-data for the teams playing on the current day
                team = team_abbs[row[0]]
                if team in teams_data:
                    #find current team's daily opponent
                    if team in schedule[curr_day_sched_format]:
                        oppo = schedule[curr_day_sched_format][team]
                        if oppo in non_reversed_def:
                            teams_data[team]['DEF'] = non_reversed_def[oppo]['DEF']
                        else:
                            teams_data[team]['DEF'] = ''
                    else:
                        teams_data[team]['DEF'] = 'UNSCHEDULED GAME'
                
    #write to file
    with open('dataset_complete.csv', mode='a', newline='') as data_file:
        data_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        #TODO flexible dates (test dates are 8/1 and 7/25-7/31)
        header_1 = ['Score From '+curr_day_sched_format, '', 'Team Hitting Stats from '+past_week_sched_format, '', '', '', '', '', 'Ill take care of this', '', '', '', '', '', '', 'Team Bullpen Stats From '+past_week_sched_format, '', '', '', '', '', '', 'Defense', 'Ill take care of these', '', '', '', '', '', '', ]
        header_2 = ['Runs', 'Team', 'BB%', 'K%', 'ISO', 'BABIP', 'wOBA', 'wRAA', 'Expected IP', 'WHIP', 'BABIP', 'LOB', 'FIP-', 'xFIP-', 'SIERA', 'Expected IP', 'WHIP', 'BABIP', 'LOB%', 'FIP-', 'xFIP-', 'SIERA', 'DEF', 'Temp', 'Wind', 'In', 'Out', 'Across', 'Dome', 'Rain']
        data_writer.writerow(header_1)
        data_writer.writerow(header_2)

        for team in teams_data:
            data_writer.writerow([teams_data[team]['runs'],
                                    team, 
                                    teams_data[team]['BB%'],
                                    teams_data[team]['K%'],
                                    teams_data[team]['ISO'],
                                    teams_data[team]['BABIP_BAT'],
                                    teams_data[team]['wOBA'],
                                    teams_data[team]['wRAA'],
                                    '',
                                    '',
                                    '',
                                    '',
                                    '',
                                    '',
                                    '',
                                    '',
                                    teams_data[team]['WHIP'],
                                    teams_data[team]['BABIP_PITCH'],
                                    teams_data[team]['LOB%'],
                                    teams_data[team]['FIP-'],
                                    teams_data[team]['xFIP-'],
                                    teams_data[team]['SIERA'],
                                    teams_data[team]['DEF']
                                    ])
        data_writer.writerow([''])

if __name__ == "__main__":
    main()

#current day
#https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=0&type=8&season=2019&month=1000&season1=2019&ind=0&team=0%2Cts&rost=0&age=0&filter=&players=0&startdate=2019-08-01&enddate=2019-08-01

#pitching 7 days
#https://www.fangraphs.com/leaders.aspx?pos=all&stats=rel&lg=all&qual=0&type=1&season=2019&month=1000&season1=2019&ind=0&team=0,ts&rost=0&age=0&filter=&players=0&startdate=2019-07-25&enddate=2019-07-31

#batting 7 days
#https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=0&type=1&season=2019&month=1000&season1=2019&ind=0&team=0,ts&rost=0&age=0&filter=&players=0&startdate=2019-07-25&enddate=2019-07-31

#defense 7 days
#https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=0&type=8&season=2019&month=1000&season1=2019&ind=0&team=0,ts&rost=0&age=0&filter=&players=0&startdate=2019-07-25&enddate=2019-07-31