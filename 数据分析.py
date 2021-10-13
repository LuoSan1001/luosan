import os
import sqlite3
import operator
from collections import OrderedDict
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties


def parse(url):
    try:
        parsed_url_components = url.split('//')
        sublevel_split = parsed_url_components[1].split('/', 1)
        domain = sublevel_split[0].replace("www.", "")
        return domain
    except IndexError:
        print('URL format error!')


def analyze(results):
    i = 1

    prompt = input("[.] Type <c> to print or <p> to plot\n[>] ")

    if prompt == "c":
        with open('./history.txt', 'w') as f:
            f.write('   20 most frequently visited web sites\n')
            for site, count in sites_count_sorted.items():
                f.write('\t' + str(i) + '.  ' + site + '\n')
                i += 1

    elif prompt == "p":

        percents = results.values()
        names = results.keys()
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        plt.axes(aspect='equal')
        font = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=18)
        plt.pie(x=percents,
                labels=names,
                autopct="%.2f%%",
                pctdistance=0.6,
                labeldistance=1.1,
                radius=1.25,
                explode=(0.05, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                textprops={'fontsize': 10, 'color': 'black'},
                )

        plt.title('Chrome浏览器最常访问的20个网站', fontproperties=font, loc='center')


    else:
        print("[.] Uh?")
        quit()


if __name__ == '__main__':
    data_path = os.path.expanduser(
        '~') + r"\AppData\Local\Google\Chrome\User Data\Default"

    files = os.listdir(data_path)

    history_db = os.path.join(data_path, 'History')


    c = sqlite3.connect(history_db)

    cursor = c.cursor()

    select_statement = "SELECT urls.url, urls.visit_count FROM urls, visits WHERE urls.id = visits.url;"
    cursor.execute(select_statement)

    results = cursor.fetchall()

    sites_count = {}

    for url, count in results:
        url = parse(url)
        if url in sites_count:
            sites_count[url] += 1
        else:
            sites_count[url] = 1
    sites_count_sorted = OrderedDict(sorted(sites_count.items(), key=lambda sites_count: sites_count[1], reverse=True))
    while len(sites_count_sorted) > 20:
        sites_count_sorted.popitem()
    analyze(sites_count_sorted)
