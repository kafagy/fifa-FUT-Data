#!/usr/bin/env python
import requests, re, time
from bs4 import BeautifulSoup
import pymysql.cursors

# Runtime start
start = time.clock()
print(start)

# Connect to the database
connection = pymysql.connect(user='root', password='abc123', host='127.0.0.1', db='futhead', cursorclass=pymysql.cursors.DictCursor)

# Opening CSV file in write mode and writing column titles
csvfile = open('fifa18.csv', 'w')
csvfile.write('Name,Club,League,Position,Rating,Pace,Shooting,Passing,Dribbling,Defending,Physical\n')

# Sending request to futhead.com
session = requests.Session()
session.headers.update({'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'})
headers = { 'Content-Type': 'application/x-www-form-urlencoded',}
FutHead = session.post("http://www.futhead.com/18/players")

# Parsing the number of pages for fifa 18 players
bs = BeautifulSoup(FutHead.text, 'html.parser')
TotalPages = int(str(bs.find('span', {'class':'font-12 font-bold margin-l-r-10'})).split("of ")[1].replace("\n", "").replace(" ", "").split("</span>")[0])
print("Number of pages to be parsed: " + str(TotalPages))

# Looping through all pages to retrieve players stats and information
for page in range(1,TotalPages):
        FutHead = session.get("http://www.futhead.com/18/players/?page=" + str(page) + "&bin_platform=ps")
        bs = BeautifulSoup(FutHead.text, 'html.parser')
        Stats = bs.findAll('span', {'class':'player-stat stream-col-60 hidden-md hidden-sm'})
        Names = bs.findAll('span', {'class':'player-name'})
        Information = bs.findAll('span', {'class':'player-club-league-name'})
        Ratings = bs.findAll('span', {'class':re.compile('revision-gradient shadowed font-12 fut18')})

        # Calcualting the number of players per page
        num = len(bs.findAll('li', {'class':'list-group-item list-group-table-row player-group-item dark-hover'}))

        # List Intialization
        playerName = []
        playerClub = []
        playerLeague = []
        playerPosition = []
        playerRating = []
        pace = []
        shooting = []
        passing = []
        dribbling = []
        defending = []
        physical = []

        # Parsing all players stats
        for stat in Stats:
            Attr = str(stat).split('<span class="hover-label">')[1].split('</span>')[0]
            score = str(stat).split('<span class="player-stat stream-col-60 hidden-md hidden-sm"><span class="value">')[1].split('</span>')[0]
            if Attr == "PAC":
                    pace.append(score)
            elif Attr == "SHO":
                    shooting.append(score)
            elif Attr == "PAS":
                    passing.append(score)
            elif Attr == "DRI":
                    dribbling.append(score)
            elif Attr == "DEF":
                    defending.append(score)
            elif Attr == "PHY":
                    physical.append(score)

        # Parsing all players information
        for i in range(0, num):
                playerName.append(str(Names[i]).split('<span class="player-name">')[1].split("</span>")[0])
                playerRating.append(str(Ratings[i]).split('">')[1].split('</span>')[0])
                playerPosition.append(str(Information[i]).split("<strong>")[1].split("</strong>")[0])
                playerClub.append(str(Information[i]).split("<strong>")[1].split("</strong>")[1].replace("\n", "").split("|")[1].replace("                         ", ""))
                playerLeague.append(str(Information[i]).split("<strong>")[1].split("</strong>")[1].replace("\n", "").split("|")[2].replace("                         ", "").split("</span>")[0].replace("                    ", ""))

        # Writing the parsed values to the DB and a CSV file
        for i in range(0, num):
                with connection.cursor() as cursor:
                        # Inserting players stats and information into the DB
                        cursor.execute('INSERT INTO futhead.fifa18 (names, club, league, position, rating, pace, shooting, passing, dribbling, defending, physical, loaddate) VALUES ("' + playerName[i].decode('utf-8').encode('latin-1', 'ignore') + '", "' + playerClub[i] + '", "' + playerLeague[i] + '", "' + playerPosition[i] + '", ' + playerRating[i] + ', ' + pace[i] + ', ' + shooting[i] + ', ' + passing[i] + ', ' + dribbling[i] + ', ' + defending[i] + ', ' + physical[i] + ', NOW());')

                        # Writingn to CSV file
                        csvfile.write(playerName[i] + "," + playerClub[i] + "," + playerLeague[i] + "," + playerPosition[i] + "," + playerRating[i] + "," + pace[i] + "," + shooting[i] + "," + passing[i] + "," + dribbling[i] + "," + defending[i] + ","  + physical[i] + "\n")

        # Commit MYSQL statements
        connection.commit()
        print("page " + str(page) + " is done!")

# Closing connection to the DB and closing csv file
connection.close()
csvfile.close()

# Runtime end
print(time.clock() - start)