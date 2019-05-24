#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 13 09:03:51 2019

@author: isaactrussell
"""

import random
from numpy import *
from time import sleep
import pandas as pd

def play(names, decider = input, num_games = 5):
    i = 0
    game = Game()
    for name in names:
        game.addPlayer(name)
    while i < num_games:
        game.dealCards()
        game.gameRound(decider)
        game.comparision()
        game.endGame()
        i += 1
        if i == 1:
            results = pd.DataFrame([list(game.roundOut.values())], columns = list(game.roundOut.keys()))
        else:
            add = pd.DataFrame([list(game.roundOut.values())], columns = list(game.roundOut.keys()))
            results = results.append(add)
    return results
        

class Game:
    
    def __init__(self):
        self.players = []
        self.num_players = 0
        self.decksUsed = 1
        self.deck = Deck()
        self.sleepTime = 0
        self.names = []
        self.results = pd.DataFrame()
        
    def addPlayer(self, name):
        self.players.append(Player(name))
        self.num_players = size(self.players)
    
    def dealCards(self):
        for player in self.players:
            self.names.append(player.name)
            
        if self.names[-1] != "**Dealer**":
            self.players.append(Player('**Dealer**'))
            self.dealer = self.players[-1]
            
        self.roundOut = {"Shown Card": 0, "Win": False, "Push": False, "Num Hits": 0, "BlackJack": False, "Final Total": 0, \
                         "Initial Total": 0, "Dealer Final Total": 0, "Dealer BlackJack": False, "Bust": False, \
                         "Dealer Bust": False}
        for j in range(2):
            for player in self.players:
                out = self.deck.dealCard()
                player.addCard(out)
        self.shown = self.dealer.cards[-1]
        self.roundOut["Shown Card"] = self.shown.val 
        for card in self.players[0].cards:
            if card.val < 10:
                self.roundOut["Initial Total"] += card.val
            else:
                self.roundOut["Initial Total"] += 10
               
    def gameRound(self, decider = input):
        if self.dealer.total == 21 and size(self.dealer.cards) == 2:
                self.roundOut["Dealer BlackJack"] = True
#            print("{} - Dealer BlackJack :(".format(self.dealer.total))
#                self.dealer.showHand()
        else:
            for player in self.players:
                if player.name != self.dealer.name:
#                    print("Dealer Showing: {} of {}\n".format(self.shown.val, self.shown.suit))
#                    print("\t{} - {}".format(player.name, player.total))
#                    player.showHand()
                    self.playerActions(player, decider)
                else:
                    self.dealerActions()
                    
    def playerActions(self, player, decider):
            while True:
                if player.total != 21:
                    if decider == input:
                        print('\nHit h for hit and s for stand') 
                        action = input()
                    else:
                        action = decider(self, player)
                        
                    if action == 's':
                        break
                    elif action == 'h':
                        out = self.deck.dealCard()
                        player.addCard(out)
                        self.roundOut["Num Hits"] += 1
#                        print("Dealer Showing: {} of {}\n".format(self.dealer.cards[1].val, self.dealer.cards[1].suit))
#                        print("\t{} - {}".format(player.name, player.total))
                        player.showHand()
                        if player.total > 21:
#                            print('\n\n\n{} - Bust! :(\n'.format(player.total))
                            self.roundOut["Bust"] = True
                            sleep(self.sleepTime)
                            break
#                        else:
#                            print(player.total)
                    if player.total == 21:
#                        print('{} - BlackJack!\n'.format(player.total))
#                        self.roundOut["BlackJack"] = True
                        break
                else:
                    if size(player.cards == 2):
    #                    print('{} - BlackJack!\n'.format(player.total))
                        self.roundOut["BlackJack"] = True
                        sleep(self.sleepTime)
                        break
                    else: 
                        break
        
    def dealerActions(self):
#        print("{}'s Turn".format(self.dealer.name))
        while True:
            total = self.dealer.total
            if total < 17:
                out = self.deck.dealCard()
                self.dealer.addCard(out)
            elif total > 21:
#                print("Dealer Bust - {}".format(total))
#                self.roundOut["Dealer Bust"] = True
                self.dealer.showHand()
#                print("")
#                self.dealer.total = 0.5
                break
            else:
#                print("Dealer Shows - {}".format(total))
                self.dealer.showHand()
#                print("")
                break
            
    def comparision(self):
        self.roundOut["Final Total"] = self.players[0].total
        self.roundOut["Dealer Final Total"] = self.dealer.total
        if self.dealer.total == 21:
            self.roundOut["Dealer BlackJack"] = True
        for player in self.players:
            if player.total > 21:
                if player.name != self.dealer.name:
                    player.total = 0
                    self.roundOut["Bust"] = True
                else:
                    self.roundOut["Dealer Bust"] = True
                    player.total = 0.5
        outcomes = array([player.total for player in self.players])
        playersOut = outcomes[:-1] > outcomes[-1]
        for player in self.players[:-1]:
            if player.total > self.dealer.total:
#                print("{} Wins! - {}".format(player.name, player.total))
                player.history["Wins"] += 1
                self.roundOut["Win"] = True
            elif player.total == self.dealer.total:
#                print("{} Pushes - {}".format(player.name, player.total))
                player.history["Pushes"] += 1
                self.roundOut["Push"] = True
            else:
                pass
#                print("{} Loses - {}".format(player.name, player.total))
            player.history["Games Played"] += 1

                
    def endGame(self):
        for player in self.players:
            player.cards = []
            player.total = 0
        if self.deck.num_cards < self.num_players*6:
            self.deck = Deck()
            self.decksUsed += 1
        if self.dealer.total == 21:
            self.roundOut["Dealer BlackJack"] = True
#        print(self.players[0].history)
            
                           
class Player:
    
    def __init__(self, name):
        self.name = name
        self.cards = []
        self.total = 0
        self.history = {"Wins": 0, "Pushes": 0, "Games Played": 0}
    
    def addCard(self, card):
        self.cards.append(card)
        
        if card.val > 10:    
            self.total = self.total + 10
        else:
            if card.val == 1:
                if self.total + 11 > 21:
                    self.total = self.total + card.val
                else:
                    self.total = self.total + 11
            else:
                self.total = self.total + card.val
        
    def showHand(self):
        for card in self.cards:
#            print("\t    {} of {}".format(card.val, card.suit))
            pass
              
class Deck:

    suits = ['Spades', 'Clubs', 'Diamonds', 'Hearts']
    class Card:

        def __init__(self, val, suit):
            
            self.suit = suit
                
            if val < 1 or val > 13:
                print('Invalid Value')
            else:
                self.val = val
            self.info = {'Suit': self.suit, 'Value': self.val}
        
    def __init__(self, num_shuffle = 5, num_decks = 5):
        
        decks = []
        for i in range(num_decks):
#            print(i)
            ##### ONE DECK #####
            cards = []
            for suit in self.suits:
                for i in range(1, 14):
                    cards.append(self.Card(i, suit))
            decks.append(cards)
            ####################
        self.cards = self.flatten(decks)
        self.num_deck = num_decks
        self.num_cards = size(self.cards)
        for _ in range(num_shuffle):
            random.shuffle(self.cards)
    
    flatten = lambda self, l: [item for sublist in l for item in sublist]
        
    def printCards(self):
        for card in self.cards:
            print(card.info)
            
    def dealCard(self):
#        print('{} of {}'.format(self.cards[0].val, self.cards[0].suit))
        out = self.cards[0]
        self.cards = self.cards[1:]
        self.num_cards = size(self.cards)
        return out

#game = Game()
#
#game.addPlayer('Isaac')
##game.addPlayer('Troy')
##game.addPlayer('Jackie')
#i = 0
#while i < 5:
#    game.dealCards()
#    #game.gameRound(decider = decisionFunction)
#    game.gameRound()
#    game.comparision()
#    game.endGame()
#    i += 1
        
#def decisionFunction(game, player):
#    if game.shown.val <= 6 or game.shown.val != 1:
#        if player.total <= 10:
#            return 'h'
#        else:
#            return 's'
#    else:
#        if player.total < 17:
#            return 'h'
#        else:
#            return 's'
#            
#roundOut = play(["Isaac"], decisionFunction, num_games = 1)
#print(roundOut)
        
roundOUt = 