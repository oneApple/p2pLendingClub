from scipy import spatial
from scipy.cluster.hierarchy import linkage
import numpy as np

class Classify:
    def __init__(self,rmatrix,level = 3):
        self.__rmatrix = np.swapaxes(rmatrix,0,1)
        self.__classPair = []
        self.__level = level
    
    def getLinkResult(self):
        distance = spatial.distance.pdist(self.__rmatrix)
        _ma = spatial.distance.squareform(distance)
        self.__linkresult = linkage(_ma,method="ward",metric = "euclidean")
        for _pair in self.__linkresult:
            self.__classPair.append(_pair[:2])
    
    def getPairMap(self):
        _num = len(self.__rmatrix)
        _pairMap = {}
        for _index in range(_num):
            _pairMap[_index] = [_index,]
        _curindex = len(self.__classPair) + 1
        for _pair in self.__classPair:
            if len(_pairMap) == self.__level:
                break
            _pairMap[_curindex] = _pairMap[int(_pair[0])] + _pairMap[int(_pair[1])]
            _curindex += 1
            del _pairMap[int(_pair[0])]
            del _pairMap[int(_pair[1])]
        return _pairMap
    
    def getSingleNum(self,index,dataMatrix):
        _reslist = []
        print self.__pairList
        for _group in self.__pairList:
            _res = 0
            _num = float(len(_group))
            for _element in _group:
                _res += dataMatrix[index][_element]
            _reslist.append(_res / _num)
        return _reslist
        
    def getSingleLabel(self,userlist):
        _reslist = []
        for _group in self.__pairList:
            _res = ""
            for _element in _group:
                _res += userlist[_element] + "\n"
            _reslist.append(_res)
        return _reslist
    
    def getShowMatrix(self,userlist,dataMatrix):
        self.__showMatrix = []
        for _index in range(0,3):
            self.__showMatrix.append(self.getSingleNum(_index, dataMatrix))
        self.__showMatrix.append(self.getSingleLabel(userlist))
    
    def ComputeResult(self,userlist,dataMatrix):
        self.getLinkResult()
        _pairMap = self.getPairMap()
        self.__pairList = []
        for _key in _pairMap:
            self.__pairList.append(_pairMap[_key])
        self.getShowMatrix(userlist, dataMatrix)
        return self.__showMatrix,self.__linkresult
    

if __name__=='__main__':
    data  = [[0.1,1,0.1],
        [0.2,3,0.4],
        [0.2,4,1],
        [0.2,2,0.2],
        [2,3,4],
        [2,0.4,0.1],
        [2,2,2]]
    d = [[1,2,3,4,5,6],[1,2,3,4,5,6],[1,2,3,4,5,6]]
    c = Classify(data)
    user = ['a','b','c','d','e','f']
    print c.ComputeResult(user,d)
