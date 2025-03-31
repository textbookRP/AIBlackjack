import numpy as np

class Model:
    def __init__(self, weights, vals, bias):
        self.weights = weights
        self.vals = vals
        self.bias = bias
        
    def relu(self, a):
        return np.maximum(0,a)
    
    def compute(self):
        nodes = np.array([self.vals])
        
        for layer in self.weights:
            matrix = np.array(layer)
            nodes = nodes.dot(matrix)
            for node in nodes:
                node = self.relu(node - self.bias)

        if nodes[-1][0] > nodes[-1][1]:
            return 0
        else:
            return 1
