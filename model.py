import numpy as np

class Model:
    def __init__(self, weights, vals, bias):
        self.weights = weights
        self.vals = vals
        self.bias = bias
        
    def compute(self):
        nodes = np.array([self.vals])
        
        for i, layer in enumerate(self.weights):
            matrix = np.array(layer)
            nodes = nodes.dot(matrix)
            nodes = np.maximum(0, (nodes - self.bias[i]))

        if nodes[-1][0] > nodes[-1][1]:
            return 0
        else:
            return 1
