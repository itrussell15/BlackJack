#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 16 09:50:00 2019

@author: isaactrussell
"""

from blackJack import play
import pandas as pd
import os

def decisionFunction(game, player):
    if game.shown.val <= 6 and game.shown.val != 1:
        if player.total <= 11:
            return 'h'
        else:
            return 's'
    else:
        if player.total < 17:
            return 'h'
        else:
            return 's'
        
def storeResults(results):
    output = os.getcwd() + "/data.csv"
    if os.path.exists(output):
        data = pd.read_csv(output)
        with open(output, 'a') as f:
            results.to_csv(output, mode = 'a', header = False)
    else:
        data = results.to_csv(output)

while True:        
    results = play(["Isaac"], decisionFunction, num_games = 500)
    storeResults(results)
    print(results)

#results = play(["Isaac"], decisionFunction, num_games = 100)
#storeResults(results)
#print(results)
