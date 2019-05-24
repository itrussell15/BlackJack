#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 16 10:17:41 2019

@author: isaactrussell
"""

import pandas as pd
from numpy import * 
import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
plt.style.use('ggplot')

location = os.getcwd() + "/data.csv"
data = pd.read_csv(location)

info = dict()
info["Num Games"] = size(data["Win"])
info["Win %"] = sum(data["Win"])/size(data["Win"])*100
info["Average # Hit"] = (sum(data["Num Hits"])/size(data["Num Hits"]))
info["Bust %"] = (sum(data["Bust"])/size(data["Bust"]))*100
info["BlackJack %"] = (sum(data["BlackJack"])/size(data["BlackJack"]))*100
info["Push %"] = (sum(data["Push"])/size(data["Push"]))*100
info["Dealer Bust %"] = (sum(data["Dealer Bust"])/size(data["Dealer Bust"]))*100
info["Shown Frequency"] = empty(13)
info["Win by Card"] = empty_like(info["Shown Frequency"])

for val in range(1,14):
    info["Shown Frequency"][val - 1] = data[data["Shown Card"] == val].shape[0]
    info["Win by Card"][val - 1] = data[(data["Shown Card"] == val) & (data["Win"] == True)].shape[0]

info["Win by Card"] = (info["Win by Card"]/info["Shown Frequency"])*100
cards = arange(1, 14)

shownVal = [data[data["Shown Card"] == val] for val in range(1,11)]
info["3D Plot Info"] = empty((10, 19))

#aces = shownVal[0]
#aces2 = data[data["Initial Total"] == 2]
#aces2win = (sum(aces2[aces2["Win"] == True].shape[0])/aces2.shape[0])*100
for i, shown in enumerate(shownVal):
    for j, total in enumerate(range(data["Initial Total"].min(), data["Initial Total"].max() + 1)):
        current = shown[shown["Initial Total"] == total]
        info["3D Plot Info"][i][j] = (current[current["Win"] == True].shape[0]/current.shape[0])*100
shown = arange(1, 11)
total = arange(data["Initial Total"].min(), data["Initial Total"].max() + 1)
        
fig = plt.figure()
fig.suptitle('BlackJack Win Percentages', fontsize=16)
ax1 = fig.add_subplot(111, projection='3d')
xpos = empty_like(info["3D Plot Info"])
for i, _ in enumerate(info["3D Plot Info"]):
    xpos[i] = [i + 1 for _ in range(19)]

xpos = xpos.flatten()
ypos = array([arange(19) for _ in range(10)]).flatten()
zpos = zeros_like(xpos)
dx = ones_like(xpos)
dy = ones_like(dx)
dz = info["3D Plot Info"].flatten()

ax1.bar3d(xpos, ypos, zpos, dx, dy, dz, color='#00ceaa')
#fig.title("Black Win Percentage Breakdown")
ax1.set_xlabel('Dealer Card Shown')
ax1.set_ylabel('2 Card Total')
ax1.set_zlabel('Win Percentage')