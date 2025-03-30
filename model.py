import numpy as np

class Model:
    def __init__(self, weights, vals):
        self.weights = weights
        self.vals = vals
        self.node_count = 0
        self.depths = [15,8,7,2]
        for i in range(len(self.depths)-1):
            self.node_count += self.depths[i]*self.depths[i+1]
        
    def relu(self, a):
        return np.maximum(0,a)

    def compute(self):
        agg = []
        agg.append(self.vals)
        rollingNodes = 0
        for i in range(len(self.depths)-1):
            temp = []
            for j in range(self.depths[i+1]):
                weightedSum = 0
                for k in range(self.depths[i]):
                    weightedSum += agg[i][k]*self.weights[rollingNodes]
                    rollingNodes += 1
                temp.append(self.relu(weightedSum))
            agg.append(temp)

        if agg[-1][0] > agg[-1][1]:
            return 0
        else:
            return 1
        """

        layer1=[]

        for i in range(self.l1depth):
            weightedSum = 0
            for j in range(3):
                weightedSum += self.vals[j]*self.weights[3*i+j]
            layer1.append(self.relu(weightedSum))

        layer2=[]

        for i in range(self.l2depth):
            weightedSum = 0
            for j in range(self.l1depth):
                weightedSum += layer1[j]*self.weights[self.l1depth*i+j+(3*self.l1depth)]
            layer2.append(self.relu(weightedSum))
        
        layer3=[]

        for i in range(self.l3depth):
            weightedSum = 0
            for j in range(self.l2depth):
                weightedSum += layer1[j]*self.weights[self.l2depth*i+j+(3*self.l1depth + self.l1depth*self.l2depth)]
            layer3.append(self.relu(weightedSum))

        layer4=[]

        for i in range(2):
            weightedSum = 0
            for j in range(self.l3depth):
                weightedSum += layer3[j]*self.weights[self.l3depth*i+j+(3*self.l1depth + self.l1depth*self.l2depth + self.l2depth*self.l3depth)]
            layer4.append(self.relu(weightedSum))"
        
        
        if layer4[0] > layer4[1]:
            return 0
        else:
            return 1"
        """