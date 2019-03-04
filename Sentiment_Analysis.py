import tweepy
from textblob import TextBlob
from tweepy import OAuthHandler
import sys
from string import punctuation
import matplotlib.pyplot as plt
import numpy as np


consumer_key = 'N61S1LzpoU4rEJRbH2LO3lF0t'
consumer_secret = 'JEZySynLHCrKW4NecFd70xHDEz9RXeVE5g5WjU8gtkrZTbktgd'
access_token='998591061961445376-n2eVFxqAdtiZO7Xz2UwPECbfKloSyo5'
access_token_secret='xOsPs8JR7wTkD4hAYY1oII3WuiZAnJN1WiN3WNY16TDvG'

auth = OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_token_secret)

api = tweepy.API(auth)

    
personalities = []
posfeed = []
negfeed = []

def personality():
    
    l = int(input("Enter number of entries: "))
    for i in range(0,l):
        n = input("Enter name: ")
        personalities.append(n)


info = {}


def checkAuth():
    print('Authorization successful\n')


def fetchData():

    t2 = ""

    non_bmp_map = dict.fromkeys(range(0x10000,sys.maxunicode+1),0xfffd)

    c = int(input("Enter the  number of tweets to be reviewed: "))

    for l in personalities:
        
        tweet_data = api.search(q = l,count = c)

        t2 = ""

        for r in tweet_data:

            text = r.text.translate(non_bmp_map)
            
            t2= str(t2)+str(text)

        info[l] = t2


def removeSpecial():
    
    special = list(punctuation)

    for l in personalities:
        
        for i in str(info[l]): 

            if i in special:

                info[l] = str(info[l]).replace(i,"")


        
def weightage():

    for r in range(0,len(personalities)):
            
        words = str(info[personalities[r]]).split("\n")

        print("\n\n%s \n=============="%(personalities[r]))

        negf = 0.0
        posf = 0.0
        c = 0

        for w in words:

            analysis = TextBlob(w)

            p = analysis.sentiment.polarity

            if p == 0.0:

                continue
                  
            elif p <= 0:
                    
                negf = negf + p
                c += abs(p)
                

            elif p >= 0:

                posf = posf + p
                c += p
                

            else:

                print(w)
                continue


        try:    
            pos = (posf/c)*100
            neg = (abs(negf)/c)*100
        except Exception as e:
            print(e)

        try:
            print("Positivity = %f"%(pos)+"%\n")
        except Exception as e:
            print(e)

        try:
            print("Negativity = %f"%(neg)+"%\n\n")
        except Exception as e:
            print(e)

        negfeed.append(abs(negf))
        posfeed.append(posf)

        

def graph():

    fig, ax = plt.subplots()
    
    width = 0.2

    index  = np.arange(len(personalities))

    b1 = plt.bar(index,posfeed,width,color = 'blue')
    b2 = plt.bar(index+width,negfeed,width,color = 'red')

    plt.ylabel('Feedback')
    plt.xlabel('Personalities')
    plt.xticks(index, personalities)
    plt.title('Twitter Sentiment Analysis')

    ax.legend((b1[0],b2[0]), ('Positive', 'Negative'))

    plt.tight_layout()
    plt.show()
        
        


checkAuth()
personality()
fetchData()
removeSpecial()
weightage()
graph()

    
