#!/usr/bin/env python

from sys import argv
import random
import twitter
import os
import APIkey as keys



def make_chains(inputtext, xgram):
    """Takes an input text as a string and returns a dictionary of
    markov chains.
    """
    text = inputtext.replace('\n', " ")
    textlist = text.strip().split()
    
    markovdict = {}

    for i in range(len(textlist) - xgram):
        key = tuple(textlist[i:i + xgram])
        value = textlist[i + xgram]
        if key not in markovdict:
            markovdict[key] = [value]
        else:
            markovdict[key].append(value)
    return markovdict


#Leaned heavily on doubledherin/FrasierLebowski in order to 
#work through 'def make_text':   
def make_text(chains, xgram):
    """Takes a dictionary of markov chains and returns random text
    based off an original text.
    """
    prefix = random.choice(chains.keys()) # returns tuple 
    suffix = random.choice(chains[prefix]) # returns str (one word)
    markovtext = ""
    for word in prefix:
        markovtext += word + " "
    markovtext += suffix + " "
    for i in range(40): #how many rounds
        newprefix = []
        for j in range(1, xgram):
            newprefix.append(prefix[j])
        newprefix.append(suffix)
        prefix = tuple(newprefix)
        suffix = random.choice(chains[prefix])
        markovtext += "{} ".format(suffix)
    return markovtext


#Some code inside 'def make_tweet' taken from doubledherin/FrasierLebowski,
#particularly the recursive portion:
def make_tweet(markovtext):
    """Takes random text, cleans up, crops to be twitter appropriate length,
    and posts to twitter.
    """
    Markovtext = markovtext.capitalize()
    Markovtextlist = Markovtext.split()
    while Markovtextlist[-1][-1] not in ".!?'":
        Markovtextlist.pop()
    for i in range (len(Markovtextlist)-1):
        if Markovtextlist[i][-1] in ".!?":
            Markovtextlist[i+1] = Markovtextlist[i+1].capitalize()
        if Markovtextlist[i] in "ii'vei'di'lli'mi...":
            Markovtextlist[i] = Markovtextlist[i].capitalize()
    tweet = (" ").join(Markovtextlist)
    if len(tweet) > 140:
        tweet = tweet[:139]
        make_tweet(tweet)
    else:
        if tweet != None:
            print tweet
            api = twitter.Api(consumer_key = keys.consumer_key,
                  consumer_secret = keys.consumer_secret,
                  access_token_key = keys.access_token_key,
                  access_token_secret = keys.access_token_secret)
            status = api.PostUpdate(tweet)
            print "Tweet tweeted successfully"
    return Markovtext


def read_files(filename1, filename2):
    file1 = open(filename1)
    inputtext = file1.read()
    file2 = open(filename2)
    inputtext += file2.read()
    file1.close()
    file2.close()
    return inputtext


def main():
    script, filename1, filename2, num = argv
    xgram = int(num)
    inputtext = read_files(filename1, filename2)
    chaindict = make_chains(inputtext, xgram)
    randomtext = make_text(chaindict, xgram)
    make_tweet(randomtext)

if __name__ == "__main__":
    main()