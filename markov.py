#!/usr/bin/env python

from sys import argv
import random
import twitter
import os
import APIkey as keys



def make_chains(input_text, x_gram):
    """Takes an input text as a string and returns a dictionary of
    markov chains."""
    text = input_text.replace('\n', " ")
    text_list = text.strip().split()
    
    markov_dict = {}

    for i in range(len(text_list) - x_gram):
        key = tuple(text_list[i:i + x_gram])
        value = text_list[i + x_gram]
        
        if key not in markov_dict:
            markov_dict[key] = [value]
        else:
            markov_dict[key].append(value)
    # print chains
    return markov_dict

def make_text(chains, x_gram):
    """Takes a dictionary of markov chains and returns random text
    based off an original text."""
    prefix = random.choice(chains.keys()) # returns tuple of x_gram words
    suffix = random.choice(chains[prefix]) # returns str - one word
    
    markov_text = ""
    for word in prefix:
        markov_text += word + " "
    markov_text += suffix + " "
    

    for i in range(40): #how many rounds
        new_prefix = []

        for j in range(1, x_gram):
            new_prefix.append(prefix[j])
        
        new_prefix.append(suffix)
        
        prefix = tuple(new_prefix)
        suffix = random.choice(chains[prefix])

        markov_text += "%s " % (suffix) #must use this format to include space
        # count = len(list(markov_text))
    return markov_text

def make_tweet(markov_text):
    Markov_text = markov_text.capitalize()
    Markov_text_list = Markov_text.split()
   
    while Markov_text_list[-1][-1] not in ".!?'":
        Markov_text_list.pop()
    
    for i in range (len(Markov_text_list)-1):
        if Markov_text_list[i][-1] in ".!?":
            Markov_text_list[i+1] = Markov_text_list[i+1].capitalize()
        if Markov_text_list[i] in "ii'vei'di'lli'mi...":
            Markov_text_list[i] = Markov_text_list[i].capitalize()
    
    tweet = (" ").join(Markov_text_list)
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
            print "Tweet tweeted!"
        
    return Markov_text

def main():
    script, filename1, filename2, num = argv
    file1 = open(filename1)
    input_text = file1.read()
    file2 = open(filename2)
    input_text += file2.read()
    x_gram = int(num)
    file1.close()
    file2.close()
    
    chain_dict = make_chains(input_text, x_gram)
    random_text = make_text(chain_dict, x_gram)
    make_tweet(random_text)
    # print twitter_text
    

if __name__ == "__main__":
    main()