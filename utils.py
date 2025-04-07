from settings import layers
import random
import numpy as np

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

def normish(x, var):
    test = random.random()
    if test > x:
        return np.random.normal(0,var)
    return np.random.normal(0,0.2)