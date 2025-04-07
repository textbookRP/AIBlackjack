import multiprocessing
from settings import modelsPerGen, threads, rounds, layers, bias
from blackjack21 import Table, Dealer
from model import Model
from utils import play_round

class Cthread(multiprocessing.Process):
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
