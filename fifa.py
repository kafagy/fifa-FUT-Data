import re
import time
import requests
import pandas as pd
import pymysql.cursors
from bs4 import BeautifulSoup

# Runtime start
start = time.clock()
print(start)

# Connect to the database
connection = pymysql.connect(user='root', password='abc123', host='127.0.0.1', db='FUTHEAD', cursorclass=pymysql.cursors.DictCursor, charset='UTF8')
cursor = connection.cursor()

tiers = [
    'gold',
    'silver',
    'bronze'
]

fifa = {
    '10': 'FIFA10',
    '11': 'FIFA11',
    '12': 'FIFA12',
    '13': 'FIFA13',
    '14': 'FIFA14',
    '15': 'FIFA15',
    '16': 'FIFA16',
    '17': 'FIFA17',
    '18': 'FIFA18'
}

for key, value in fifa.items():
    print('Doing FIFA ' + key)

    # Truncating table before inserting data into the table
    cursor.execute('TRUNCATE TABLE FUTHEAD.{};'.format(value))

    # List Intializations
    players = []
    attributes = []

    # Looping through all pages to retrieve players stats and information
    for tier in tiers:
        FutHead = requests.get('https://www.futhead.com/' + key + '/players/?level=' + tier + '&bin_platform=ps')
        bs = BeautifulSoup(FutHead.text, 'html.parser')
        TotalPages = int(re.sub('\s +', '', str(bs.find('span', {'class': 'font-12 font-bold margin-l-r-10'}).get_text())).split(' ')[1])
        print('Number of pages to be parsed for FIFA ' + key + ' ' + tier + ' level players: ' + str(TotalPages))
        for page in range(1, TotalPages + 1):
            FutHead = requests.get('http://www.futhead.com/' + key + '/players/?page=' + str(page) + '&level=' + tier + '&bin_platform=ps')
            bs = BeautifulSoup(FutHead.text, 'html.parser')
            Stats = bs.findAll('span', {'class': 'player-stat stream-col-60 hidden-md hidden-sm'})
            Names = bs.findAll('span', {'class': 'player-name'})
            Information = bs.findAll('span', {'class': 'player-club-league-name'})
            Ratings = bs.findAll('span', {'class': re.compile('revision-gradient shadowed font-12')})
            num = len(bs.findAll('li', {'class': 'list-group-item list-group-table-row player-group-item dark-hover'}))

            # Parsing all players information
            for i in range(num):
                p = []
                p.append(Names[i].get_text())
                strong = Information[i].strong.extract()
                try:
                    p.append(re.sub('\s +', '', str(Information[i].get_text())).split('| ')[1])
                except IndexError:
                    p.append('')
                try:
                    p.append(re.sub('\s +', '', str(Information[i].get_text())).split('| ')[2])
                except IndexError:
                    p.append('')
                p.append(strong.get_text())
                p.append(tier.capitalize())
                p.append(Ratings[i].get_text())
                players.append(p)

            # Parsing all players stats
            temp = []
            for stat in Stats:
                if Stats.index(stat) % 6 == 0:
                    if len(temp) > 0:
                        attributes.append(temp)
                    temp = []
                if stat.find('span', {'class': 'value'}) is None:
                    pass
                else:
                    temp.append(stat.find('span', {'class': 'value'}).get_text())
            print('Page ' + str(page) + ' is done!')

    # Inserting data into its specific table
    for player, attribute in zip(players, attributes):
        cursor.execute('''
              INSERT INTO FUTHEAD.{} (
                  NAME,
                  CLUB, 
                  LEAGUE, 
                  POSITION,
                  TIER,
                  RATING,
                  PACE,
                  SHOOTING, 
                  PASSING,
                  DRIBBLING,
                  DEFENDING,
                  PHYSICAL
              ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''.format(value), (*player, *attribute))

    # Dumping the lines into a csv file
    pd.read_sql_query('SELECT * FROM FUTHEAD.{};'.format(value), connection).to_csv(value + '.csv', sep=',', encoding='utf-8', index=False)

    # Commit MYSQL statements
    connection.commit()

# Closing connection to the DB and closing csv file
connection.close()

# Runtime end
print(time.clock() - start)
