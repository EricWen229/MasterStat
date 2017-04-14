# -*- coding: utf-8 -*-

import matplotlib.font_manager as fontConfig
import matplotlib.pyplot as plt
import numpy as np
import csv

def readFromCsv(filePath):
    with open(filePath, newline='') as f:
        reader = csv.reader(f)
        return list(reader)

def plot(title, filePath, table):
    total = np.array(table, dtype=float)
    success = np.array(list(filter(lambda x: x[-1] == '1', table)), dtype=float)
    fail = np.array(list(filter(lambda x: x[-1] == '0', table)), dtype=float)

    cutoff = float(success[-1][-2])

    totalAverage = np.average(total, axis=0)
    successAverage = np.average(success, axis=0)
    failAverage = np.average(fail, axis=0)

    # font needs to be figured for Chinese characters
    font = fontConfig.FontProperties(fname='./PingFang.ttc')

    fig, ax = plt.subplots()

    ax.set_title(title, fontproperties=font)
    ax.set_xlabel('初试成绩', fontproperties=font)
    ax.set_ylabel('复试成绩', fontproperties=font)
    ax.axis([250, 500, 250, 500])

    ax.grid(True)

    # distribution graph
    for row in success:
        ax.plot(row[0], row[5], 'b+')
    for row in fail:
        ax.plot(row[0], row[5], 'r+')

    # average
    ax.plot(successAverage[0], successAverage[5], 'bD')
    ax.plot(failAverage[0], failAverage[5], 'rD')
    ax.plot(totalAverage[0], totalAverage[5], 'mD')

    # cutoff
    ax.plot([cutoff - 500, 500], [500, cutoff - 500], 'k:')

    # labels
    ax.text(252, 314, '总人数:\t\t%d' % (len(table)), fontproperties=font)
    ax.text(252, 302, '录取率:\t\t%.2f%%' % (totalAverage[-1] * 100), fontproperties=font)
    ax.text(252, 290, '分数线:\t\t%.2f' % (cutoff), fontproperties=font)
    ax.text(252, 278, '上榜均分:\t%.2f %.2f %.2f' % (successAverage[0], successAverage[5], successAverage[-2]), fontproperties=font)
    ax.text(252, 266, '落榜均分:\t%.2f %.2f %.2f' % (failAverage[0], failAverage[5], failAverage[-2]), fontproperties=font)
    ax.text(252, 254, '总均分:\t\t%.2f %.2f %.2f' % (totalAverage[0], totalAverage[5], totalAverage[-2]), fontproperties=font)

    fig.savefig(filePath)

csScienceScore = readFromCsv('data/cs_s_sysu.csv')
seScienceScore = readFromCsv('data/se_s_sysu.csv')
csEngineerScore = readFromCsv('data/cs_e_sysu.csv')
seEngineerScore = readFromCsv('data/se_e_sysu.csv')

plot('计算机科学与技术', 'plot/cs_s_sysu.png', csScienceScore)
plot('软件工程（学术型）', 'plot/se_s_sysu.png', seScienceScore)
plot('计算机技术', 'plot/cs_e_sysu.png', csEngineerScore)
plot('软件工程', 'plot/se_e_sysu.png', seEngineerScore)

