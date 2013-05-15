import numpy as np

class CFGrayRelationWeight:
    def __init__(self,rMatrix,wlist,currentlist,futurelist):
        self.__rmatrix = rMatrix
        self.__curlist = currentlist
        self.__futlist = futurelist
        self.__wlist = wlist
        
    def getWeightList(self,rMatrix,wlist,indexlist):
        sum = 0.0
        _weightlist = []
        _matrix = []
        for index, col in zip(indexlist,rMatrix):
            sum += wlist[index]
            _matrix.append(col)
        for index in indexlist:
            _weightlist.append(wlist[index] / sum)
        return _weightlist, np.swapaxes(_matrix,0,1)
    
    def computeSingle(self,wlist,matrix):
        _grwlist = []
        for col in matrix:
            _grw = 0.0
            for index in range(len(col)):
                _grw += col[index] * wlist[index]  
            _grwlist.append(_grw)
        return _grwlist
    
    def ComputeResult(self):
        templist = []
        templist.append(self.computeSingle(*self.getWeightList(self.__rmatrix,self.__wlist, self.__curlist)))
        templist.append(self.computeSingle(*self.getWeightList(self.__rmatrix,self.__wlist, self.__futlist)))
        return templist
    
