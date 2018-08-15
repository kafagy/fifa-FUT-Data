# FIFA FUT Players Data
## What is the purpose of this script?
- The purpose of this repository is to have a script that automatically pulls down all players data from Futhead's website for all FIFA versions starting with FIFA 10.
## How to use it?
- Just run the fifa.py script:
`python3 fifa.py`
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
- Input database's host, database name, user and password in the fifa.py connection line.
- Make sure you create tables using the DDL in fifa.sql to be able to correctly encode latin literals when writing to the Database.
