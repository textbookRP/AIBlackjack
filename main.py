from blackjack21 import Table, Dealer
import random
from model import Model
import heapq
import numpy as np
import multiprocessing

random.seed()

modelsPerGen = 800
threads = 11
rounds = 8000
layers = [15,8,8,2]
bias = [6,5,3]

def normish(x, var):
    test = random.random()
    if test > x:
        return np.random.normal(0,var)
    return np.random.normal(0,0.2)

def play_round(table, player, model):
    hit = False
    while not (player.bust or player.stand):
        for i in range(len(player.hand)):
            model.vals[i+1] = player.hand[i].value

        action = model.compute()

        if action == 0:
            player.play_hit()
            hit = True

        elif action == 1:
            player.play_stand()

    return hit

def ranStart():
    interim=[]
    for layer in range(len(layers)-1):
        arr1 = []
        for node in range(layers[layer]):
            arr2 = []
            for weight in range(layers[layer+1]):
                arr2.append(random.random())
            arr1.append(arr2)
        interim.append(arr1)
            

    return interim


def train(start, delta):

    variations = []

    for i, item in enumerate(start):
        variations.append(item)
        allocated = 0.2
        if i == 0:
            allocated = 0.6
        for i in range(round((allocated*modelsPerGen)-1)):
            delta2 = normish(0.5, 2.5)
            interim = []

            for layer in item:
                arr1 = []
                for node in layer:
                    arr2 = []
                    for weight in node:
                        arr2.append(weight+(delta2*delta*normish(0.96, 1.3)))
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
        workers.append(cthread(variations[bounds[i]:bounds[i+1]], i, scoresd, hitsd, cashd))

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


class cthread(multiprocessing.Process):
    def __init__(self, vars, num, scoresd, hitsd, cashd):
        multiprocessing.Process.__init__(self)
        self.tscores = []
        self.vars = vars
        self.num = num
        self.scoresd = scoresd
        self.hitsd = hitsd
        self.cashd = cashd

    def get(self):
        return self.tscores
    
    def run(self):
        self.tempScores = []
        self.tempHits = []
        self.tempCash = []
        for start in self.vars:
            net_gain = 0
            hits = 0
            for i in range(rounds):
                a = ("AI", 10)
                players = (a, )
                table = Table(players)

                dealer_first_card = table.dealer.hand[0]

                vals = [dealer_first_card.value, table.players[0].hand[0].value, table.players[0].hand[1].value, 0,0,0,0,0,0,0,0,0,0,0,0]

                model = Model(start, vals, bias)

                for player in table:
                   r = play_round(table, player, model)

                if r == True:
                    hits += 1

                table.dealer.play_dealer()
                #show_result(table)

                if table.players[0].result > 0:
                    net_gain += 1
                elif table.players[0].result < 0:
                    net_gain -= 1

            self.tempCash.append(net_gain)
            
            net_gain += (10000*rounds)/((hits+10)*(hits-rounds-10))
            net_gain = round(net_gain)

            self.tempScores.append(net_gain)
            self.tempHits.append(hits)
        self.scoresd[self.num] = self.tempScores
        self.hitsd[self.num] = self.tempHits
        self.cashd[self.num] = self.tempCash

def main():
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
        workers.append(cthread(startNetwork[bounds[i]:bounds[i+1]], i, scoresd, hitsd, cashd))

    for item in workers:
        item.start()
    
    for item in workers:
        item.join()

    for i in range(threads):
        scores += scoresd[i]
        hits += hitsd[i]
        cash += cashd[i]

    print(f"winner was {scores.index(max(scores))} with {max(scores)} (cash: {cash[scores.index(max(scores))]}, hits: {hits[scores.index(max(scores))]}) with this generation having a mean of {round(np.mean(scores))} (cash: {round(np.mean(cash))}, hits: {round(np.mean(hits))})")

    final = []
    for i in range(3):
        final.append(startNetwork[scores.index(heapq.nlargest(3, scores)[i])])

    startPoint = final
    i=4

    while True:
        interim = train(startPoint, 1/((i)+100))
        startPoint = interim
        i+=1
        if i % 20 == 0:
            print(startPoint[0])

if __name__ == "__main__":
    main()


