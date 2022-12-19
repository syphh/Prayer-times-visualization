import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import requests
from datetime import datetime
from bs4 import BeautifulSoup

table = []
for month in range(1, 13):
    data_url = f'https://timesprayer.com/en/list-prayer-in-algiers-2022-{month}.html'
    data = requests.get(data_url)
    soup = BeautifulSoup(data.text)
    rows = soup.find('tbody').find_all('tr')
    for row in rows:
        table.append([td.text for td in row.find_all('td')])

df = pd.DataFrame(table, columns=['date', 'fajr', 'chourouk', 'dhuhr', 'asr', 'maghrib', 'isha'])
df.to_csv('prayer_times.csv', index=False)
