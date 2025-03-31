from blackjack21 import Table, Dealer
import random
from model import Model
import heapq
import numpy as np
import multiprocessing

random.seed()

modelsPerGen = 150
threads = 4
rounds = 2000
layers = [15,8,8,2]
bias = 1

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

    for type in start:
        variations.append(type)
        for i in range(round((modelsPerGen/3)-1)):
            delta2 = normish(0.7, 1)
            interim = type
            for layer in interim:
                for node in layer:
                    for weight in node:
                        weight += delta2*delta*normish(0.9, 0.8)
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
    return [variations[scores.index(heapq.nlargest(3, scores)[0])], variations[scores.index(heapq.nlargest(3, scores)[1])], variations[scores.index(heapq.nlargest(3, scores)[2])]]


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
            
            net_gain -= (0.0000006*(((rounds/2)-hits)**2))**3
            net_gain = round(net_gain)

            self.tempScores.append(net_gain)
            self.tempHits.append(hits)
        self.scoresd[self.num] = self.tempScores
        self.hitsd[self.num] = self.tempHits
        self.cashd[self.num] = self.tempCash

def main():
    startNetwork = []
    for i in range(round(modelsPerGen)):
        startNetwork.append(ranStart())
    
    scores = []

    for start in startNetwork:

        net_gain = 0
        hits = 0

        for i in range(rounds):
            a = ("AI", 1)
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
        net_gain -= (0.0000006*(((rounds/2)-hits)**2))**3
        net_gain = round(net_gain)
        scores.append(net_gain)
        print(f"{startNetwork.index(start)} net win: {net_gain} and {hits} hits")
    print(f"winner was {scores.index(max(scores))} with {max(scores)} and {hits} hits")

    startPoint=[startNetwork[scores.index(heapq.nlargest(3, scores)[0])], startNetwork[scores.index(heapq.nlargest(3, scores)[1])], startNetwork[scores.index(heapq.nlargest(3, scores)[2])]]

    i=4
    while True:
        startPoint = train(startPoint, 1/((i)+100))
        i+=1
        if i % 80 == 0:
            print(startPoint)
    print(startPoint)

if __name__ == "__main__":
    main()


