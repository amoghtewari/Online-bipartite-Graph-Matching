import pandas as pd
import numpy as np
import random
import sys
from collections import defaultdict

# setting seed
random.seed(0)

def BidScaler(bid, rembudget, budget):
    xu = (budget - rembudget) / budget
    return bid * psi(xu)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Enter greedy, balance or msvv as second system argument!")
    else:
        input = pd.read_csv('bidder_dataset.csv')
        # advertiser->budget
        budget1 = dict()
        # keyword->bid
        bids = defaultdict(dict)

        bidderData = pd.read_csv('bidder_dataset.csv')

        for i in range(0, len(bidderData)):
            advertiser=bidderData.iloc[i][0]
            keyword=bidderData.iloc[i][1]
            bidVal=bidderData.iloc[i][2]
            budVal=bidderData.iloc[i][3]

            #add advertisers and their budgets to budget dictionary
            if advertiser not in budget1:
                budget1[advertiser]=budVal

            #create dictionaries for keywords that are not in bids dictionary
            if keyword not in bids:
                bids[keyword]={}

            #add current advertisers bid to the current keyword-advertiser
            #for item in bids:
                #if item != advertiser:
                    #bids[keyword][advertiser] = bidVal

            if advertiser not in bids[keyword]:
                bids[keyword][advertiser]=bidVal

        with open('queries.txt') as f:
            queries = f.readlines()
        queries = [x.strip() for x in queries]

        def check_budget(b):
            keys = []
            for key in b.keys():
                keys.append(key)

            for advtsr in keys:
                if budget[advtsr] >= b[advtsr]:
                    return 0
            return -1

        def psi(x):
            return 1 - np.exp(x - 1)


    if sys.argv[1] == 'greedy':

        revenue = 0.0
        budget=dict(budget1)
        def greedyBidder(b,q):
            keys = []
            for key in b[q].keys():
                keys.append(key)
            maxBidder = keys[0]
            maxBid = 0
            c = check_budget(b[q])
            if c == -1:
                return -1
            for k in keys:
                if budget[k] >= b[q][k]:
                    if maxBid < b[q][k]:
                        maxBidder = k
                        maxBid = b[q][k]
                    elif maxBid == b[q][k]:
                        if maxBidder > k:
                            maxBidder = k
                            maxBid = b[q][k]
            return maxBidder

        for q in queries:
            possibleBidder = greedyBidder(bids,q)
            if possibleBidder != -1:
                revenue = revenue + bids[q][possibleBidder]
                budget[possibleBidder]=budget[possibleBidder] - bids[q][possibleBidder]

        print(revenue)
        print(revenue/sum(budget1.values()))


    elif sys.argv[1] == 'balance':

        revenue = 0.0
        budget = dict(budget1)
        def balanceBidder(b,q):
            keys = []
            for key in b[q].keys():
                keys.append(key)
            maxBidder = keys[0]
            c = check_budget(b[q])
            if c == -1:
                return -1
            for k in keys:
                if budget[k] >= b[q][k]:
                    if budget[maxBidder] < budget[k]:
                        maxBidder = k
                    elif budget[maxBidder] == budget[k]:
                        if maxBidder > k:
                            maxBidder = k

            return maxBidder
        for q in queries:
            possibleBidder = balanceBidder(bids,q)
            if possibleBidder != -1:
                revenue = revenue + bids[q][possibleBidder]
                budget[possibleBidder]=budget[possibleBidder] - bids[q][possibleBidder]

        print(revenue)
        print(revenue/sum(budget1.values()))


    elif sys.argv[1] == 'msvv':
        revenue = 0.0
        budget = dict(budget1)
        #budget2 = dict(budget1)

        def msvvBidder(b, q):
            keys = []
            for key in b[q].keys():
                keys.append(key)
            maxBidder = keys[0]
            c = check_budget(b[q])
            if c == -1:
                return -1
            for k in keys:
                if budget1[k] >= b[q][k]:
                    m1 = BidScaler(b[q][maxBidder], budget[maxBidder], budget1[maxBidder])
                    m2 = BidScaler(b[q][k], budget[k], budget1[k])
                    if m1 < m2:
                        maxBidder = k
                    elif m1 == m2:
                        if maxBidder > k:
                            maxBidder = k

            return maxBidder

        for q in queries:
            possibleBidder = msvvBidder(bids,q)
            if possibleBidder != -1:
                revenue = revenue + bids[q][possibleBidder]
                budget[possibleBidder]=budget[possibleBidder] - bids[q][possibleBidder]

        print(revenue)
        print(revenue / sum(budget1.values()))

    else:
        print('Invalid Input')
