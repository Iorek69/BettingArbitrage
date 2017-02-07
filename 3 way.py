from urllib.request import urlopen
import requests
import urllib
from bs4 import BeautifulSoup
import heapq
import re
import numpy
import datetime
import time

arbOpCompilation = []
participantNamesList = []
semiFinalPrint = []
finalPrint =[]
Vendor = []
VendorS = ['Bet365','SkyBet','Totesport','BoyleSport','Betfred','SportingBet','BetVictor','Paddypower','StanJames','888sport',
           'Ladbrokes','Coral','WilliamHill','Winner','BetFair','Betway','BetBright','Unibet','Bwin','32Red','10Bet','Marathon','BetFair',
           'Exchange','Betdaq','Matchbook']

''' Calls the final tally calculations '''
def calculateFinalTally():
    print('----FINAL TALLY----')
    print(str(datetime.datetime.now()))

    if not len(finalPrint) == 0:
        print("AVERAGE2: ","%.2f" % numpy.mean(finalPrint), "%")
        print("MAX: ","%.2f" % numpy.max(finalPrint), "%")
        print('-------------------')
    else:
        print('No arbitrage scenarios found')
    print('-------------------')
    # time.sleep(5)

''' Initiate the Scraper and collect the data'''
def Scraper(URLsToCheck, URLcounter):
    global arbOpCompilation
    global participantNamesList
    global semiFinalPrint
    global finalPrint
    global VendorS
    global Vendor

    URL = URLsToCheck[URLcounter]
    ' This will print the current page being scraped'
    # print(URLsToCheck[URLcounter])
    response = requests.get(URL)
    soup = BeautifulSoup(response.content,"html.parser")

    i = 0
    compilation = []
    for game in soup.findAll("span", {"class":"odds"}):
        odds = (''.join(game.findAll(text=True)))
        if "(" in odds:
            odds = odds[2:]
            odds = odds[:-1]
            delimited = odds.split("/")
            delimited = list(map(int, delimited))
            if len(delimited) == 1:
                delimited.append(1)
            europeanOdds = (delimited[0]/delimited[1])+1

            inverseEuropeanOdds = 1/europeanOdds
            compilation.append(inverseEuropeanOdds)
            i = i + 1

    # right after here calculate whether arb or not
    lenC = len(compilation)
    counter = 0
    counteri = 0
    while counter < lenC:
        VendorsRate = compilation[counter]+compilation[counter + 1]+compilation[counter + 2]
        if VendorsRate < 1: # criteria for arb

            arbOp = VendorsRate - 1 # calculates percentage as removed from 100
            arbOpPercent = (-arbOp*100) # calculates as percentage
            arbOpCompilation.append(arbOpPercent) # adds percentage to array

            if arbOpPercent > 1: #1% is accepted to be the minimum acceptable percentage

                participants = soup.findAll("span", {"class":"fixtures-bet-name"})[counter]
                participantName1 = (''.join(participants.findAll(text=True)))

                participants = soup.findAll("span", {"class":"fixtures-bet-name"})[counter+2]
                participantName2 = (''.join(participants.findAll(text=True)))

                # findID = soup.findAll("tr",{"class":"match-on"})[counteri+1]#["data-market-id"]
                gameURL = soup.findAll("a",{"class":"button btn-1-small"})[counteri+1]["href"]
                gameURL = "http://www.oddschecker.com"+gameURL

                # Calculate the % of the bet to make
                p1bet = ((compilation[counter]))*(100+arbOpPercent)
                dbet = ((compilation[counter+1]))*(100+arbOpPercent)
                p2bet = ((compilation[counter+2]))*(100+arbOpPercent)

                # print(gameURL)
                print('Win', participantName1, ': lay', "%.2f" % p1bet,'% of principal')
                print('Draw', ': lay', "%.2f" % dbet,'% of principal')
                print('Win', participantName2, ': lay', "%.2f" % p2bet,'% of principal')
                print("%.2f" % arbOpPercent, '%', 'profit')
                # print(str(datetime.datetime.now()))
                print('-------------------')
                # finalPrint.append(arbOpPercent)

        counter = counter + 3
        counteri = counteri + 1

''' Initiates the URLs to scrape and a timer if necessary '''
def TimerOnScraper():

    URLcounter = 0
    URLsToCheck = ['http://www.oddschecker.com/football',
                   'http://www.oddschecker.com/football/english/premier-league',
                   'http://www.oddschecker.com/football/english/championship']#,
##                   'http://www.oddschecker.com/football/scottish/premiership',
##                   'http://www.oddschecker.com/football/scottish/championship',
##                   'http://www.oddschecker.com/football/germany/bundesliga',
##                   'http://www.oddschecker.com/football/germany/bundesliga-2',
##                   'http://www.oddschecker.com/football/france/ligue-1',
##                   'http://www.oddschecker.com/football/france/ligue-2',
##                   'http://www.oddschecker.com/football/italy/serie-a',
##                   'http://www.oddschecker.com/football/italy/serie-b',
##                   'http://www.oddschecker.com/football/spain/la-liga-primera',
##                   'http://www.oddschecker.com/football/world-cup',
##                   'http://www.oddschecker.com/football/champions-league',
##                   'http://www.oddschecker.com/football/europa-league']

    while URLcounter < len(URLsToCheck):
        Scraper(URLsToCheck, URLcounter)
        arbOpCompilation = []
        # print(arbOpCompilation)
        URLcounter = URLcounter + 1

for i in range(0,1):
    TimerOnScraper()
print('Finished')
input()
