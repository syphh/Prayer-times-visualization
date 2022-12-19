import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import requests
from datetime import datetime
from bs4 import BeautifulSoup


def time_to_minutes(t):
    h, m = datetime.strftime(datetime.strptime(t, '%I:%M %p'), '%H:%M').split(':')
    return 60*int(h) + int(m)


def hover(event):
    vis = vline.get_visible()
    if event.inaxes == plt.gca():
        vline.set_xdata([event.xdata, event.xdata])
        vline.set_visible(True)
        data = df.iloc[int(event.xdata), [0, 1, 3, 4, 5, 6]]
        for i in range(len(texts)):
            if i == 0:
                texts[i].set_text(data[i])
                texts[i].set_y(1470)
                texts[i].set_x(event.xdata-20)
            else:
                texts[i].set_text('{:02d}:{:02d}'.format(data[i]//60, data[i]%60))
                texts[i].set_y(data[i]+20)
                texts[i].set_x(event.xdata+1)
            texts[i].set_visible(True)
        plt.gcf().canvas.draw_idle()
    else:
        if vis:
            vline.set_visible(False)
            for text in texts:
                text.set_visible(False)
            plt.gcf().canvas.draw_idle()


df = pd.read_csv('prayer_times.csv')
for time in ['fajr', 'chourouk', 'dhuhr', 'asr', 'maghrib', 'isha']:
    df[time] = df[time].apply(lambda t: time_to_minutes(t))

plt.style.use('bmh')
plt.figure(figsize=(10, 4))
plt.xlim([0, 364])
plt.xticks(np.array([15, 29, 30, 30.5, 30.5, 30.5, 30.5, 30.5, 30.5, 30.5, 30.5, 30.5]).cumsum())
plt.gca().set_xticklabels(['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec'])
plt.ylim([0, 1440])
plt.yticks(range(0, 1440, 120))
plt.gca().set_yticklabels(["{:02d}:00".format(t) for t in range(0, 24, 2)])
end_pos = df.iloc[-1, [1, 3, 4, 5, 6]]
names = ['fajr', 'dhuhr', 'asr', 'maghrib', 'isha']
for i in range(len(names)):
    plt.text(df.shape[0]+2, end_pos[i]-20, names[i].capitalize())
vline, = plt.plot([0, 0], [0, 1440], c='black', zorder=float('inf'))
vline.set_visible(False)
texts = [plt.text(0, 0, '') for _ in range(6)]
for text in texts:
    text.set_visible(False)
plt.gcf().canvas.mpl_connect("motion_notify_event", hover)
for time in names:
    plt.plot(df.index, df[time])
plt.xlabel('Days')
plt.ylabel('Time')
plt.show()
