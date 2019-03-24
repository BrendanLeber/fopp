#!/usr/bin/env python
# -*- coding: utf-8 -*-


def strip_punctuation(value):
    punctuation_chars = ["'", '"', ",", ".", "!", ":", ";", "#", "@"]
    for ch in punctuation_chars:
        value = value.replace(ch, "")
    return value


# list of positive words to use
positive_words = []
with open("positive_words.txt") as pos_f:
    for lin in pos_f:
        if lin[0] != ";" and lin[0] != "\n":
            positive_words.append(lin.strip())


# list of negative words to use
negative_words = []
with open("negative_words.txt") as pos_f:
    for lin in pos_f:
        if lin[0] != ";" and lin[0] != "\n":
            negative_words.append(lin.strip())


def get_pos(text):
    num_positive = 0
    for word in text.split():
        if strip_punctuation(word.lower()) in positive_words:
            num_positive += 1
    return num_positive


def get_neg(text):
    num_negative = 0
    for word in text.split():
        if strip_punctuation(word.lower()) in negative_words:
            num_negative += 1
    return num_negative


twitter_data = []
with open("project_twitter_data.csv") as inf:
    for line in inf:
        twitter_data.append(line.strip().split(","))
    twitter_data = twitter_data[1:]  # skip header


with open("resulting_data.csv", "w") as outf:
    outf.write("Number of Retweets, Number of Replies, Positive Score, Negative Score, Net Score\n")
    for tweet in twitter_data:
        pos_score = get_pos(tweet[0])
        neg_score = get_neg(tweet[0])
        net_score = pos_score - neg_score
        outf.write("{0},{1},{2},{3},{4}\n".format(tweet[1], tweet[2], pos_score, neg_score, net_score))
