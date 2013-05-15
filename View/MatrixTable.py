# -*- coding: UTF-8 -*-
import wx.grid
class MatrixTable(wx.grid.PyGridTableBase):
    def __init__(self,matrix = [],collabel = [],rowlabel = []):
        wx.grid.PyGridTableBase.__init__(self)
        self.__data = matrix
        self.__rowLabels = rowlabel
        self.__colLabels = collabel        
         
    def GetNumberRows(self):
        return len(self.__data)
 
    def GetNumberCols(self):
        return len(self.__data[0])
 
    def IsEmptyCell(self, row, col):
        return False
 
    def GetValue(self, row, col):
        return self.__data[row][col]
 
    def SetValue(self, row, col, value):
        pass
         
    def GetColLabelValue(self, col):#列标签
        return self.__colLabels[col]
        
    def GetRowLabelValue(self, row):#行标签
        return self.__rowLabels[row]
 
 
