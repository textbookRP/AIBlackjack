from blackjack21 import Table, Dealer
import random
from model import Model
import heapq
import numpy as np
import multiprocessing

random.seed()

modelsPerGen = 350
threads = 7
rounds = 8000

class cthread(multiprocessing.Process):
    def __init__(self, vars, num, scoresd, hitsd):
        multiprocessing.Process.__init__(self)
        self.tscores = []
        self.vars = vars
        self.num = num
        self.scoresd = scoresd
        self.hitsd = hitsd

    def get(self):
        return self.tscores
    
    def run(self):
        self.tempScores = []
        self.tempHits = []
        for start in self.vars:
            net_gain = 0
            hits = 0
            for i in range(rounds):
                a = ("AI", 10)
                players = (a, )
                table = Table(players)

                dealer_first_card = table.dealer.hand[0]

                vals = [dealer_first_card.value, table.players[0].hand[0].value, table.players[0].hand[1].value, 0,0,0,0,0,0,0,0,0,0,0,0]

                model = Model(start, vals)

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

            self.tempScores.append(net_gain)
            self.tempHits.append(hits)
        self.scoresd[self.num] = self.tempScores
        self.hitsd[self.num] = self.tempHits

def ranStart(model):
    interim=[]
    for i in range(model.node_count):
        interim.append(random.random())
    return interim

def print_cards(player):
    print(f"\n{player.name}")
    for i, card in enumerate(player.hand):
        if (type(player) != Dealer) or (type(player) == Dealer and i == 0):
            print(f"{card.rank} of {card.suit}")
    if type(player) != Dealer:
        print(player.total)


def play_round(table, player, model):
    #print_cards(table.dealer)
    #print_cards(player)
    hit = False
    while not (player.bust or player.stand):
        for i in range(len(player.hand)):
            model.vals[i+1] = player.hand[i].value
        action = model.compute()
        if action == 0:
            player.play_hit()
            hit = True
            #print_cards(player)
        elif action == 1:
            player.play_stand()
    return hit


def show_result(table):
    print_cards(table.dealer)
    print(f"\nDealer has {table.dealer.total}")
    for player in table:
        result = player.result

def train(start, delta):
    variations = []
    for type in start:
        variations.append(type)
        for i in range(round((modelsPerGen/3)-1)):
            interim = []
            for weight in type:
                interim.append(weight + delta*np.random.normal(0,0.3))
            variations.append(interim)

    manager = multiprocessing.Manager()
    scoresd = manager.dict()
    hitsd = manager.dict()

    scores = []
    hits = []

    workers = []

    bounds = [0]

    for i in range(threads):
        bounds.append(round((modelsPerGen/threads)*i))

    for i in range(threads):
        workers.append(cthread(variations[bounds[i]:bounds[i+1]], i, scoresd, hitsd))

    for item in workers:
        item.start()
    
    for item in workers:
        item.join()

    for i in range(threads):
        scores += scoresd[i]
        hits += hitsd[i]

    print(f"winner was {scores.index(max(scores))} with {max(scores)}, with this generation having a mean of {np.mean(scores)} and {hits[scores.index(max(scores))]} hits")
    return [variations[scores.index(heapq.nlargest(3, scores)[0])], variations[scores.index(heapq.nlargest(3, scores)[1])], variations[scores.index(heapq.nlargest(3, scores)[2])]]

def main():
    startNetwork = []
    for i in range(round(modelsPerGen/2)):
        startNetwork.append(ranStart(Model(None, None)))
    
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

            model = Model(start, vals)

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
        startPoint = train(startPoint, 1/((i)+60))
        i+=1
        if i % 80 == 0:
            print(startPoint)
    print(startPoint)

if __name__ == "__main__":
    main()

