from blackjack21 import Table, Dealer
import random
from model import Model
import heapq
import numpy as np
import multiprocessing

random.seed()

modelsPerGen = 1000
threads = 11
rounds = 16000
layers = [15,12,6,2]
bias = [6,4,1.5]

start = [[[0.3601483895043599, 0.7258091095664023, 0.09908827290233733, 0.0742155739525317, 0.018035487601406452, 0.2559417804949173, 0.28611170165248495, 0.1982178165792441, 1.0083272828775725, 0.2968011008353497, 1.0734474074815006, 0.16043145372228432], [0.2981527461608858, 0.8040022413708802, 0.9217925663949698, 0.9277685111951821, 0.49164991009117576, 0.6742489413223091, 0.7341879577344753, 0.20269112018529067, 0.6675476946438627, 0.07575431712818656, 0.6246992871522572, 0.7231202658817498], [-0.11046094509714612, 0.5141622973058416, 0.19211219371773625, 0.7624482559860719, 0.5654724505207929, 0.27154354905753014, 0.11882031010135773, 0.8728967786300648, 0.4940335944056676, 1.0253067820451032, 1.0059295996635456, 0.2604066954996891], [0.4973391078270233, 0.11086816356196443, 0.3287911191486453, 0.0827867348471788, 0.5137257062680399, 0.738432606947084, 0.4397834444625775, 0.3877101397530281, 0.36498804954292857, 0.5270558122006144, 0.7102478579821386, 0.2939961634121796], [0.946403577335497, 0.3006679662556201, 0.2763368705200709, -0.10978315554060905, 0.3878160266929165, 0.16146383146852913, 0.5863088352410549, 0.7874989715657676, 0.4643294854130426, 0.2516699170287618, 0.27709263303172277, 0.9541021765036454], [0.2811260444138717, 0.3908150678790929, 0.5975252134293894, 0.20002157671188808, 0.11836267688120815, 0.8225671457224256, 0.07458226370158678, 0.2737988177848503, 0.31798243464582376, 0.6753582246094024, 0.6588506987420611, 0.8637213960325454], [0.20521310025978226, 0.6009912052526883, 0.6188968224895514, 0.8672133861601542, 0.8562176087200215, 0.13016986359502705, 0.9448273009554481, 0.4391007963369083, 0.7466096895737309, 0.25501197120847274, 0.5084767495166292, 0.22309191143224355], [0.796270196584117, -0.007546918258427453, 0.7861152773417329, 0.8101376712834971, 0.9558817464368203, 0.6183830727997276, 0.3160734547646486, 0.3800710557499461, 0.4959962451129371, 0.24433237602343605, 0.3216446129373459, 0.858003479689726], [0.8647481373041939, 0.3347050227029283, 0.4250247321438485, 0.7866896351543201, 0.3639483982170988, 0.8044310147345176, 0.03813337021005317, 0.42459142464170946, 0.8376875936351101, 0.12437404110623305, 0.7777164458523361, 0.8092019804020468], [0.07330935073912202, 0.6112678373559537, 0.9787992838295801, -0.06886995539011032, 1.0042909425239996, 0.3888051858038859, 0.4960539063969308, 0.592368147030725, 0.9054283514338987, 0.05777731074749909, 0.227834656708587, 0.5764140531210252], [0.7898473862026273, 0.6060453978023261, 0.5712747568894578, 0.9845481436107353, 0.5368006743379115, 0.8116837713427322, 0.6678115732177112, 0.8466238407733231, 0.8935327567448011, 0.44745553955884954, 0.590689235255939, 0.6040971970701053], [0.794726053388162, 0.8807057747395619, 0.31412263479571534, 0.9868302738616345, 0.18119992974270344, 0.319267892278481, 0.15320070039498493, 0.2636519685470633, 0.389929422357442, 0.7584135398127517, 0.4788551382806681, 0.6197318495894402], [0.125675784675891, 0.9910253889966942, 0.3523832403189897, 0.8647851307109119, 0.4259610961429926, 0.6302553735548203, 0.3467865328362685, 0.44177430009274943, 0.5572884133712016, 0.6590154258243234, 0.48328027793052575, 0.03159260248458947], [0.641606871985986, 0.8660058871895516, 0.8700887378316653, 0.2157981519513071, 0.2394524122771326, 0.5370822577026271, 0.7379680342880225, 0.5426543380052775, 0.6877203109803052, 0.7650093140589911, 0.1978772508381348, 0.8721225020300991], [0.4427324612377068, 0.6400842076907723, 0.3855392817421753, 1.062432124919002, 0.3314587556564729, 0.21097598787032235, 0.8957801888263979, -0.06722381887197398, 0.14445257529772335, 0.8584458204064994, 0.5233667098334801, 0.837388250412743]], [[0.9173527088100978, -0.06124147168366093, 0.29922967834304537, 0.8771134204130234, 0.18484608274380182, 0.18166134040491888], [1.006456582293617, 0.34983001191349855, 0.2494319849077754, 0.313253001525301, 0.5792040505216997, 0.43257952060059734], [0.22119036287978136, 0.15576663771832333, -0.008471404345162525, 0.6030125523679061, 0.6203292231114942, 0.1318146464097556], [1.0076875329339967, 0.21379192258142313, 0.6532487054666162, -0.011056299527470172, 0.45565988882094277, 0.9628671597338865], [0.257588048863422, 0.1354559404613831, 0.419614896015402, 0.18968474272444286, 0.9561923544046924, 0.199853497890445], [0.41305148681139287, 0.6220762150575506, 0.34259497083611096, 0.3920301055440798, 0.4960702882067425, 0.4166173107094561], [0.8842342106483915, 0.8934323922121015, 0.6689432483532827, 0.4482063392112775, 0.5961872663745222, 0.7092678657020538], [1.0280267992205079, 0.5730267210704528, 0.7757054324922192, 0.9233312498784125, 0.7061226265742848, 0.740051041056319], [0.24107965655012945, -0.007677819844235362, 0.11038854871961051, 0.6942454161598522, 0.19200141409009214, 0.5917582597222805], [0.27200083220605825, 0.19419546044266145, 0.6305205919947555, 0.7469183192233669, 0.9056653603877218, 0.9634718119211093], [0.9701695994493642, 0.372495030144767, 0.455756913443185, 0.32582387400154056, 0.34030095743413435, 0.8040095277775041], [0.8594490216853511, 0.5983957017134929, 0.7144004896342625, 0.9399539907618317, 0.7844607610961858, 0.5531310557809875]], [[0.47000340312111105, 0.013557595128331273], [0.21638666654698233, 0.22549294221589122], [0.16455714244317632, 0.8452141915788108], [0.644782486652187, 0.7188514894062014], [0.15900861608392472, 0.8791338885438199], [0.46732354328924, -0.025155695032546437]]]

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
            delta2 = normish(0.5, 4)
            interim = []

            for layer in item:
                arr1 = []
                for node in layer:
                    arr2 = []
                    for weight in node:
                        arr2.append(weight+(delta2*delta*normish(0.98, 1)))
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


