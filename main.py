from blackjack21 import Table, Dealer
import random
from model import Model
import heapq
import numpy as np
import multiprocessing
from cthread import Cthread
from settings import *
from utils import ranStart, normish

random.seed()

def train(start, delta):

    variations = []

    for i, item in enumerate(start):
        variations.append(item)
        allocated = 0.2
        if i == 0:
            allocated = 0.6
        for i in range(round((allocated*modelsPerGen)-1)):
            delta2 = normish(delta2Prob, delta2VarDefault, delta2VarTrigger)
            interim = []

            for layer in item:
                arr1 = []
                for node in layer:
                    arr2 = []
                    for weight in node:
                        arr2.append(weight+(delta2*delta*normish(normishProb, normishVarDefault, normishVarTrigger)))
                    arr1.append(arr2)
                interim.append(arr1)

        
            variations.append(interim)


    manager = multiprocessing.Manager()
    scoresd = manager.dict()
    hitsd = manager.dict()
    cashd = manager.dict()

    scores = []
    hits = []
    cash = []

    workers = []

    bounds = [0]

    for i in range(threads):
        bounds.append(round((modelsPerGen/threads)*i))

    for i in range(threads):
        workers.append(Cthread(variations[bounds[i]:bounds[i+1]], i, scoresd, hitsd, cashd))

    for item in workers:
        item.start()
    
    for item in workers:
        item.join()

    for i in range(threads):
        scores += scoresd[i]
        hits += hitsd[i]
        cash += cashd[i]

    print(f"winner was {scores.index(max(scores))} with {max(scores)} (cash: {cash[scores.index(max(scores))]}, hits: {hits[scores.index(max(scores))]}) with this generation having a mean of {round(np.mean(scores))} (cash: {round(np.mean(cash))}, hits: {round(np.mean(hits))})")
    #print(scores[50])
    final = []
    for i in range(3):
        final.append(variations[scores.index(heapq.nlargest(3, scores)[i])])
    return final

def main():
    final = []

    if start == None:
        startNetwork = []
        for i in range(round(modelsPerGen*3)):
            startNetwork.append(ranStart())

        manager = multiprocessing.Manager()
        scoresd = manager.dict()
        hitsd = manager.dict()
        cashd = manager.dict()

        scores = []
        hits = []
        cash = []

        workers = []

        bounds = [0]

        for i in range(threads):
            bounds.append(round((modelsPerGen/threads)*i))

        for i in range(threads):
            workers.append(Cthread(startNetwork[bounds[i]:bounds[i+1]], i, scoresd, hitsd, cashd))

        for item in workers:
            item.start()
        
        for item in workers:
            item.join()

        for i in range(threads):
            scores += scoresd[i]
            hits += hitsd[i]
            cash += cashd[i]

        print(f"winner was {scores.index(max(scores))} with {max(scores)} (cash: {cash[scores.index(max(scores))]}, hits: {hits[scores.index(max(scores))]}) with this generation having a mean of {round(np.mean(scores))} (cash: {round(np.mean(cash))}, hits: {round(np.mean(hits))})")

        for i in range(3):
            final.append(startNetwork[scores.index(heapq.nlargest(3, scores)[i])])
    else:
        for i in range(3):
            final.append(start)

    startPoint = final
    i=4

    while True:
        interim = train(startPoint, 1/(100))
        startPoint = interim
        i+=1
        if i % 20 == 0:
            print(startPoint[0])

if __name__ == "__main__":
    main()


