import pylab as pl

class PolyGraph:
    def __init__(self,xlist,ylist,polylist):
        self.__xlist = xlist
        self.__ylist = ylist
        self.__polylist = polylist
    
    def Draw(self,title,xlabel,ylabel,legendlist):
        for _poly,_legend in zip(self.__polylist,legendlist):
            pl.plot(_poly,label = _legend,)
        pl.xlabel(xlabel)
        pl.ylabel(ylabel)
        pl.title(title)
        pl.grid(True)#wang ge
        pl.legend(loc = "upper left")#labe
        pl.xticks(range(len(self.__xlist)),self.__xlist)
        pl.yticks(self.__ylist)
        pl.show()
        
if __name__=='__main__':
    import numpy as np 
    ylist = np.arange(0,1,0.1)
    xlist = ['a','b','c','d','e']
    polylist = [[0.2,0.4,0.6,0.8,1],[0.1,0.3,0.5,0.7,0.9]]
    p = PolyGraph(xlist,ylist,polylist)
    p.Draw("title", "xlabel", "ylabel",["label","labe"])

