from scipy.cluster.hierarchy import dendrogram
import pylab

class Aggregation:
    def __init__(self,linkres,xlabel):
        self.__link = linkres
        self.__xlabel = xlabel
    
    def Draw(self,title,xlabel,ylabel):
        pylab.figure(figsize= (15,10))
        res = dendrogram(self.__link)
        _max = len(res['ivl']) * 10 + 5
        pylab.xlabel(xlabel)
        pylab.ylabel(ylabel)
        pylab.title(title)
        pylab.grid(True)#wang ge
        pylab.legend(loc = "upper left")#labe
        _label = []
        for index in res['ivl']:
            _label.append(self.__xlabel[int(index)])
        pylab.xticks(range(5,_max,10),_label)
        pylab.show()
    
    
    
            
