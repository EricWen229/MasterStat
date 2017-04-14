# -*- coding: utf-8 -*-

import csv

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

def parseColumn(rawColumn):
    return rawColumn.get_text().translate({
        ord('是'): '1',
        ord('否'): '0',
        ord('\n'): None
    })

def parseRow(rawRow):
    rawColumns = rawRow.find_all('td')
    columns = list(map(lambda column: parseColumn(column), rawColumns))[5:]
    return columns

def parseTable(rawTable):
    rawRows = rawTable.find_all('tr')
    return list(map(lambda row: parseRow(row), rawRows))

def parsePage(soup):
    rawTables = soup.find_all('table')
    return list(map(lambda table: parseTable(table), rawTables))

def writeCsv(fileName, table):
    with open(fileName, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(table)

url = 'http://sdcs.sysu.edu.cn/content/2824'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh;'
    ' Intel Mac OS X 10_12_4) AppleWebKit/'
    '537.36 (KHTML, like Gecko) Chrome/57.'
    '0.2987.133 Safari/537.36'
}
request = Request(url=url, headers=headers)
response = urlopen(request)
html = response.read()
soup = BeautifulSoup(html, 'html.parser')
tables = parsePage(soup)

csScienceScore = tables[3]
seScienceScore = tables[4]
csEngineerScore = tables[6][:-1]
seEngineerScore = tables[7][:-1]

writeCsv('data/cs_s_sysu.csv', csScienceScore[2:])
writeCsv('data/se_s_sysu.csv', seScienceScore[2:])
writeCsv('data/cs_e_sysu.csv', csEngineerScore[2:])
writeCsv('data/se_e_sysu.csv', seEngineerScore[2:])

