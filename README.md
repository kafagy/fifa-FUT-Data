[![HitCount](http://hits.dwyl.io/kafagy/fifa-FUT-Data.svg)](http://hits.dwyl.io/kafagy/fifa-FUT-Data)
# FIFA FUT Players Data
## What is the purpose of this script?
- The purpose of this repository is to have a script that automatically pulls down all players data from Futhead's website for all FIFA versions starting with FIFA 10. And to pull detialed data from Futbin.com
## How to use it?
- Just run the fifa.py script:
`python3 futbin.py` to get Futbin data.
`python3 futhead.py` to get FutHead data.
## Players data ouput format:
- After running the script the user will have the data saved in a MySQL database and CSV files.
# Requirements:
- Python 3
- MySQL
- PIP
### You will need to use PIP to install the following libraries:
- pymysql
- bs4
- requests
- pandas
#### Note:
- You will need to sucessfully run the futhead.sql script before running the futhead.py parser.
- Input database's host, database name, user and password in the futhead.py connection line.
- Make sure you create tables using the DDL in futhead.sql to be able to correctly encode latin literals when writing to the Database.
