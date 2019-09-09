from util import entropy, information_gain, partition_classes
import numpy as np
import ast

class DecisionTree(object):
    def __init__(self):
        # Initializing the tree as an empty dictionary or list, as preferred
        #self.tree = []
        self.tree = {}
        pass

    def learn(self, X, y):
        # TODO: Train the decision tree (self.tree) using the the sample X and labels y
        #If all classifications are constant, then you can stop splitting

        if len(set(y))==1:
            self.tree['node'] = 'leaf'
            self.tree['label'] = y[0]
            return

        else:
            #Each non-leaf node must be split in a way that maximises info gain and minimises entropy
            #Initialize variables
            maximum_ig = {}
            x_left = []
            x_right = []
            y_left = []
            y_right = []

            #Determining max info gain
            for i in range(len(X[0])):
                for j in list(set([row[i] for row in X])):
                    xl,xr,yl,yr = partition_classes(X,y,i,j)
                    if len(y)!=len(yl) and len(y)!=len(yr):
                        maximum_ig[information_gain(y,[yl,yr])] = [i,j]

            split_attr=maximum_ig[max(maximum_ig.keys())][0]
            split_val=maximum_ig[max(maximum_ig.keys())][1]

            #Make Decision tree based on generated split val and attributes
            xl,xr,yl,yr = partition_classes(X,y,split_attr,split_val)
            self.tree['left'] = DecisionTree()
            self.tree['right'] = DecisionTree()
            self.tree['right'].learn(xr,yr)
            self.tree['left'].learn(xl,yl)
            self.tree['node'] = 'node'
            self.tree['attribute'] = split_attr
            self.tree['value'] = split_val
        pass


    def classify(self, record):
        # TODO: classify the record using self.tree and return the predicted label
        if self.tree['node'] == 'leaf':
            return self.tree['label']
        else:
            if type(record[self.tree['attribute']]) == int or type(record[self.tree['attribute']]) == float:
                if record[self.tree['attribute']] <= self.tree['value']:
                    return self.tree['left'].classify(record)
                else:
                    return self.tree['right'].classify(record)
            else:
                if record[self.tree['attribute']] == self.tree['value']:
                    return self.tree['left'].classify(record)
                else:
                    return self.tree['right'].classify(record)
