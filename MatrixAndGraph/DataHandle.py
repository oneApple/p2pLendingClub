# -*- coding: UTF-8 -*-
import StandardProcess ,RelationCoefficient, QuotaWeight, GrayRelationWeight, CFGrayRelationWeight, Classify

class DataHandle:
    def __init__(self):
        pass
    
    def GetFileData(self,path):
        self.__originData = []
        with open(path,'r') as f:
            for line in f:
                if line != "\n":
                    col = line[:-1].split(",")
                    self.__originData.append(col)
        import copy
        self.__rowlabel = copy.deepcopy(self.__originData[0])
        for col in range(1,len(self.__originData)):
            for row in range(len(self.__originData[col])):
                try:
                    self.__originData[col - 1][row] = float(self.__originData[col][row].strip())
                except ValueError, e:
                    print self.__originData[col - 1][row],e
        del self.__originData[len(self.__originData) - 1]
        return self.__rowlabel
    
    def ComputeGrayRelationResult(self,typelist,curlist,futlist):
        s = StandardProcess.StandardProcess(self.__originData,typelist)
        self.__standardData = s.ComputeResult()
        
        optlist = [1,] * len(self.__standardData[0])
        r = RelationCoefficient.RelationCoefficient(self.__standardData,optlist)
        self.__GrayRelationData = r.ComputeResult()
        
        q = QuotaWeight.QuotaWeight(self.__standardData)
        self.__quotaData = q.ComputeResult()
        
        g = GrayRelationWeight.GrayRelationWeight(self.__GrayRelationData,self.__quotaData[3])
        self.__grayRelationWeightData = g.ComputeResult()
        c = CFGrayRelationWeight.CFGrayRelationWeight(self.__GrayRelationData,self.__quotaData[3],curlist,futlist)
        self.__grayRelationWeightData += c.ComputeResult()
        self.formMap()
        
    def ComputeLinkResult(self,userlist):    
        _classfiydata = []
        self.__computedata = []
        self.__userlabe = []
        
        _grayRelationDelSortNum = []
        for _index in range(len(self.__grayRelationWeightData) / 2):
            _grayRelationDelSortNum.append(self.__grayRelationWeightData[_index * 2])
        
        import numpy as np
        for _index in userlist:
            _classfiydata.append(np.swapaxes(self.__GrayRelationData,0,1)[_index])
            self.__computedata.append(np.swapaxes(_grayRelationDelSortNum,0,1)[_index])
            self.__userlabe.append(self.__rowlabel[_index])
        
        self.__c = Classify.Classify(np.swapaxes(_classfiydata,0,1))  
        linkres = self.__c.getLinkResult() 
        from GlobalData.MagicNum import DataMap
        self.__dataMap[DataMap.SIX_LINKRESULT] = linkres
        return self.__userlabe
        
    def ComputeAggregationResult(self,level):
        import numpy as np
        aggres = self.__c.ComputeResult(self.__userlabe,np.swapaxes(self.__computedata,0,1),level)
        from GlobalData.MagicNum import DataMap
        self.__dataMap[DataMap.SEVEN_AGGREGATION] = aggres
        return aggres
        
    def formMap(self):
        from GlobalData.MagicNum import DataMap
        self.__dataMap = {DataMap.ZERO_ROWLABEL:self.__rowlabel,
                          DataMap.ONE_ORIGINAL:self.__originData,
                          DataMap.TWO_STANDARD:self.__standardData,
                          DataMap.THREE_GRCOEFFICIENT:self.__GrayRelationData,
                          DataMap.FOUR_QUOTAWEIGHT:self.__quotaData,
                          DataMap.FIVE_GRWEIGHT:self.__grayRelationWeightData}
    
    def GetData(self,type):
        return self.__dataMap[type]

if __name__=='__main__': 
        from GlobalData.MagicNum import QuotaTable ,DataMap
        typelist = [QuotaTable.POSITIVE_RELATION,
                    QuotaTable.POSITIVE_RELATION,
                    QuotaTable.NEGATIVE_RELATION,
                    QuotaTable.NEGATIVE_RELATION,
                    QuotaTable.NEGATIVE_RELATION,
                    QuotaTable.POSITIVE_RELATION,
                    QuotaTable.POSITIVE_RELATION,
                    QuotaTable.POSITIVE_RELATION,
                    QuotaTable.POSITIVE_RELATION,
                    ]

        d =  DataHandle()
        d.GetFileData("../data.plc")  
        d.ComputeResult(typelist,[0,1,2],[3,4,5,6,7],3,[0,1,2,3,4,5,6,7,8,9,10,11])
        import Aggregation
        a = Aggregation.Aggregation(d.GetData(DataMap.SIX_LINKRESULT),[x for x in range(1,13)])
        a.Draw("title", "xlabel", "ylabel")