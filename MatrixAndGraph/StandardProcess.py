from GlobalData import MagicNum

class StandardProcess:
    def __init__(self,matrix,typelist):
        self.__matrix = matrix
        self.__typelist = typelist
    
    def computeNumerator(self,type,x,min,max):
        if type == MagicNum.QuotaTable.POSITIVE_RELATION:
            return x - min
        elif type == MagicNum.QuotaTable.NEGATIVE_RELATION:
            return max - x

    def computeStandard(self,col,min,max,type):
        for index,x in enumerate(col):
            col[index] = self.computeNumerator(type,x,min,max) / (max - min)
    
    def ComputeResult(self):
        import copy
        tempmatrix = copy.deepcopy(self.__matrix)
        for col ,type in zip(tempmatrix,self.__typelist):
            self.computeStandard(col, min(col), max(col), type)
        return tempmatrix