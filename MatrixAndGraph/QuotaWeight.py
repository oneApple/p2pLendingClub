import numpy as np

class QuotaWeight:
    def __init__(self,matrix):
        self.__matrix = matrix
    
    def computeChangeCoefficient(self):
        self.__stddev = []
        self.__mean = []
        self.__cclist = []
        for col in self.__matrix:
            _stddev = np.std(col)
            _mean = np.mean(col)
            self.__mean.append(_mean)
            self.__stddev.append(_stddev)
            self.__cclist.append(_stddev / _mean)
        self.__res = []
        self.__res.append(self.__stddev)
        self.__res.append(self.__mean)
        self.__res.append(self.__cclist)
        
    def ComputeResult(self):
        self.computeChangeCoefficient()
        _totalcc = np.sum(self.__cclist)
        self.__qwlist = []
        for _cc in self.__cclist:
            _qw = _cc / _totalcc
            self.__qwlist.append(_qw)
        self.__res.append(self.__qwlist)
        return self.__res