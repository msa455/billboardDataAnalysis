# -*- coding: utf-8 -*-
"""
Created on Mon May 31 22:52:57 2021

@author: pmjum
"""

from bs4 import BeautifulSoup
import requests
import os
import datetime
import time
import pandas as pd



weeks = ["2021-05-29", "2021-05-22", "2021-05-15"]

#TODO: Add logic checking if the file exists and what state it is at
outputFile = "billboardData.csv"
 
#A helper function that pings google to check if our connection is offline. 
def checkConnection():
    #ping google, if response, return True
    return True

#get names of the artists and songs from between the brackets
def getNames(text):
    text = text.replace(">","<")
    text = text.split("<")
    return(text[2])

#add all of the info for that week to an array and return the array
def addWeek(week, names, artists,rankNumbers):
    allData = []
    for i in range(len(names)):
        name = getNames(str(names[i]))
        if "," in name:
            name = name.replace(",", "|")
        rankNumber = getNames(str(rankNumbers[i]))
        artist = getNames(str(artists[i]))
        if "," in artist:
            artist = artist.replace(","," &amp; ")
        entry = week + "," + name + "," + artist + "," + rankNumber
        allData.append(entry)
        
    return allData

#get the songnames, artists, and rank number for a given week
def getSoup(week):
    url = "https://www.billboard.com/charts/hot-100/" + week
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    songNames = soup.find_all("span", {"class":"chart-element__information__song"})
    artists = soup.find_all("span", {"class":"chart-element__information__artist"})
    rankNumber = soup.find_all("span", {"class":"chart-element__rank__number"})
    return(songNames,artists,rankNumber)


                
def makeCSV(outputFile):
    with open(outputFile, "w") as f:
        currentDate = datetime.date.today()
        #min Billboard Date: 1958,8,4
        minDate = datetime.date(1958,8,4)
        oneWeek = datetime.timedelta(days=7)
        while(currentDate >= minDate):
            print("fetching data for: ", str(currentDate), "...")
            songNames,artists,rankNumbers = getSoup(str(currentDate))
            data = addWeek(str(currentDate),songNames,artists,rankNumbers)
            for song in data:
                f.write(song + "\n")
            currentDate -= oneWeek
            time.sleep(2)


    
#print(getSongNames(str(songNames[0])))


#makeCSV(outputFile)

df = pd.read_csv("test.csv")

#print(df.tail(1))