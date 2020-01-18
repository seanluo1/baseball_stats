import csv

team_col = {
    'SEA': 1,
    'SF': 2,
    'OAK': 3,
    'LAD': 4,
    'LAA': 5,
    'SD': 6,
    'ARI': 7,
    'COL': 8,
    'TEX': 9,
    'HOU': 10,
    'KC': 11,
    'STL': 12,
    'MIN': 13,
    'MIL': 14,
    'CHC': 15,
    'CWS': 16,
    'DET': 17,
    'CLE': 18,
    'CIN': 19,
    'PIT': 20,
    'TOR': 21,
    'BOS': 22,
    'NYY': 23,
    'NYM': 24,
    'PHI': 25,
    'BAL': 26,
    'WAS': 27,
    'ATL': 28,
    'TB': 29,
    'MIA': 30,
}
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
csv_in = open('data/2019_matchups.csv')
csv_out = open('data/2019_matchups_fixed.csv', 'w', newline='')

writer = csv.writer(csv_out)
line_count = 0
for row in csv.reader(csv_in):
    if line_count == 0:
        line_count += 1
        writer.writerow(row)
        continue
    date = row[0][4:]
    row[0] = date
    #print(row)
    for i in range(len(row)):
        if row[i] == 'LA':
            row[i] = 'LAD'
        if row[i] != '' and len(row[i]) < 4:
            #print(row[i])
            row[team_col[row[i]]] = team_col_rev[i]
        
    writer.writerow(row)

# with open('data/2019_matchups.csv') as sched:
#     sched_reader = csv.reader(sched, delimiter=',')
    
#     line_count = 0
#     for row in sched_reader:
#         if line_count == 0:
#             #print(f'Column names are {", ".join(row)}')
#             line_count += 1
#         else: