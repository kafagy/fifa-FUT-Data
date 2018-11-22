import re
import json
import requests
import pandas as pd
from bs4 import BeautifulSoup

fifa = {
    '15': 'FIFA15',
    '16': 'FIFA16',
    '17': 'FIFA17',
    '18': 'FIFA18',
    '19': 'FIFA19'
}

open('FutBinCards19.csv', 'w').close()
open('FutBinDetailed19.csv', 'w').close()
for key, value in fifa.items():
    print('Doing ' + value)
    FutBin = requests.get('https://www.futbin.com/' + key + '/players', headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'})
    bs = BeautifulSoup(FutBin.text, 'html.parser')
    TotalPages = str(bs.findAll('li', {'class': 'page-item '})[-1].text).strip()
    print('Number of pages to be parsed for FIFA ' + key + ' is ' + TotalPages + ' Pages')
    for page in range(1, int(TotalPages) + 1):
        FutBin = requests.get('https://www.futbin.com/' + key + '/players?page=' + str(page), headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'})
        bs = BeautifulSoup(FutBin.text, 'html.parser')
        table = (bs.find('table', {'id': 'repTb'}))
        tbody = table.find('tbody')
        names = ([str(i.text).strip()
                             .replace('\n', ' ')
                             .split('           ')[0] for i in tbody.findAll('tr', {'class': re.compile('player_tr_\d+')})])
        cardDetails = ([str(i.text).strip()
                                   .replace('\n', ' ')
                                   .replace(' \\ ', '\\')
                                   .replace(' | ', '|').split('       ')[1]
                                   .replace(' POTM', '-POTM')
                                   .replace(' LIVE', '-LIVE')
                                   .replace(' Winner', '-Winner')
                                   .replace(' SBC', '-SBC')
                                   .replace(' Deal', '-Deal')
                                   .replace(' Base', '-Base')
                                   .replace(' Reward', '-Reward')
                                   .split() for i in tbody.findAll('tr', {'class': re.compile('player_tr_\d+')})])
        for i in range(len(names)):
            cardDetails[i].insert(0, names[i])
        webpages = ['https://www.futbin.com' + str(i['data-url']).replace(' ', '%20') for i in tbody.findAll('tr', {'class': re.compile('player_tr_\d+')})]
        overall = {}
        for webpage in webpages:
            d = {}
            json_data = ''
            profile = requests.get(webpage, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'})
            bs = BeautifulSoup(profile.text, 'html.parser')
            images = [i['src'] for i in bs.findAll('img', id=re.compile('player_nation|player_club|player_pic'))[0:3]]
            cardDetails[webpages.index(webpage)].extend(images)
            info = bs.find('div', {'id': 'info_content'})
            d.update(dict(zip([str(i.text).replace('Name', 'Fullname').strip() for i in info.findAll('th')], [str(i.text).strip() for i in info.findAll('td')])))
            detailedStats = bs.findAll('div', {'class': 'col-md-4 col-lg-4 col-6'})
            for i in detailedStats:
                d.update(dict(zip(([j.text for j in i.findAll('span', 'ig-stat-name-tooltip')]), [str(j.text).strip() for j in i.findAll('div', 'stat_val')])))
            overall[(webpages.index(webpage) + 1) * page] = d
            json_data += json.dumps(overall, indent=4, separators=(',', ': '), sort_keys=True)
        df = pd.DataFrame(cardDetails)
        df.to_csv('FutBinCards19.csv', mode='a', header=False, sep=',', encoding='utf-8', index=True)
        pd.read_json(json_data).transpose().to_csv('FutBinDetailed19.csv', mode='a', header=False, sep=',', encoding='utf-8', index=True)

# Needs some fixing in the code for RW-SBC, ST-SBC, etc in the card.csv and need to fix the 'v=9,' issue.
df1 = pd.read_csv('FutBinCards19.csv')
df2 = pd.read_csv('FutBinDetailed19.csv')
df = df1.join(df2, rsuffix='_2', on='ID')
df=df[[c for c in df.columns if c.lower()[-3:-1] != '_2']]
df.to_csv('FutBin19.csv', mode='w', header=True, sep=',', encoding='utf-8', index=False)