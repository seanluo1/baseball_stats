import csv
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
#utility function that converts percentage strings to floats
def p2f(x):
    return round(float(x.strip('%'))/100, 3)

#keep teams_data global
teams_data = {}

#extract schedule data
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

#eventually contain all code into a function
# def extractDay(curr_day_filepath, batting_filepath, pitching_filepath, defense_filepath)

#read current day runs
with open('data/curr_day.csv') as cd_file:
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
with open('data/past_week_batting.csv') as bat_file:
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
                teams_data[team]['BB%'] = p2f(row[2])
                teams_data[team]['K%'] = p2f(row[3])
                teams_data[team]['ISO'] = row[9]
                teams_data[team]['BABIP_BAT'] = row[11]
                teams_data[team]['wOBA'] = row[17]
                teams_data[team]['wRAA'] = row[16]

#read past 7 days bullpen stats
with open('data/past_week_pitching.csv') as pitch_file:
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
                oppo = schedule[' 08/1/19'][team] #TODO pass in flexible date, add in error case if not found
                
                teams_data[team]['WHIP'] = non_reversed_pitch[oppo]['WHIP']
                teams_data[team]['BABIP_PITCH'] = non_reversed_pitch[oppo]['BABIP_PITCH']
                teams_data[team]['LOB%'] = non_reversed_pitch[oppo]['LOB%']
                teams_data[team]['FIP-'] = non_reversed_pitch[oppo]['FIP-']
                teams_data[team]['xFIP-'] = non_reversed_pitch[oppo]['xFIP-']
                teams_data[team]['SIERA'] = non_reversed_pitch[oppo]['SIERA']

#read past 7 days defense stats
with open('data/past_week_defense.csv') as def_file:
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
                oppo = schedule['08/1/19'][team] #TODO pass in flexible date, add in error case if not found
                
                teams_data[team]['DEF'] = non_reversed_def[oppo]['DEF']
            
#write to file
with open('dataset.csv', mode='w', newline='') as data_file:
    data_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    #TODO flexible dates (test dates are 8/1 and 7/25-7/31)
    header_1 = ['Score From 8/1', '', 'Team Hitting Stats from 7/25-7/31', '', '', '', '', '', 'Ill take care of this', '', '', '', '', '', '', 'Team Bullpen Stats From 7/25-7/31', '', '', '', '', '', '', 'Defense', 'Ill take care of these', '', '', '', '', '', '', ]
    header_2 = ['Runs', 'Team', 'BB%', 'K%', 'ISO', 'BABIP', 'wOBA', 'wRAA', 'Expected IP', 'WHIP', 'BABIP', 'LOB', 'FIP-', 'xFIP-', 'SIERA', 'Expected IP', 'WHIP', 'BABIP', 'LOB%', 'FIP-', 'xFIP-', 'SIERA', 'DEF', 'Temp', 'Wind', 'In', 'Out', 'Across', 'Dome', 'Rain']
    data_writer.writerow(header_1)
    data_writer.writerow(header_2)

    for team in teams_data:
        #print(team)
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
                                teams_data[team]['DEF'] #TODO still need to get this somehow
                                ])

#current day
#https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=0&type=8&season=2019&month=1000&season1=2019&ind=0&team=0%2Cts&rost=0&age=0&filter=&players=0&startdate=2019-08-01&enddate=2019-08-01

#pitching 7 days
#https://www.fangraphs.com/leaders.aspx?pos=all&stats=rel&lg=all&qual=0&type=1&season=2019&month=1000&season1=2019&ind=0&team=0,ts&rost=0&age=0&filter=&players=0&startdate=2019-07-25&enddate=2019-07-31

#batting 7 days
#https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=0&type=1&season=2019&month=1000&season1=2019&ind=0&team=0,ts&rost=0&age=0&filter=&players=0&startdate=2019-07-25&enddate=2019-07-31

#defense 7 days
#https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=0&type=8&season=2019&month=1000&season1=2019&ind=0&team=0,ts&rost=0&age=0&filter=&players=0&startdate=2019-07-25&enddate=2019-07-31