import numpy as np

class RelationCoefficient:
    def __init__(self,matrix,optimallist,pCoefficient = 0.5):
        self.__matrix = matrix
        self.__pCoefficient = pCoefficient
        self.__optlist = [optimallist] * len(matrix)
        self.__minlist = []
        self.__maxlist = []
        
    def computeOptimalMaxMin(self):
        tempmatrix = np.abs(np.add(self.__matrix,np.negative(self.__optlist)))
        max = np.max(tempmatrix)
        min = np.min(tempmatrix)
        self.__numerator = min + self.__pCoefficient * max
        self.__max = self.__pCoefficient * max
        return tempmatrix
        
    def computeElement(self,col,opt):
        for index,x in enumerate(col):
            col[index] = self.__numerator / (col[index] + self.__max)
        
    def ComputeResult(self):
        self.computeOptimalMaxMin()
        tempmatrix = self.computeOptimalMaxMin()
        for col,opt in zip(tempmatrix,self.__optlist):
            self.computeElement(col, opt)
        return tempmatrix