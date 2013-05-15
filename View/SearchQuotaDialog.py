# -*- coding: UTF-8 -*-
import wx

import ValidaDialog
from GlobalData import MagicNum
from DataBase import QuotaTable

higherQuota = {MagicNum.QuotaTable.CURRENT_VALUE:'当前价值',MagicNum.QuotaTable.FUTURE_VALUE:'未来价值', \
               MagicNum.QuotaTable.NEGATIVE_RELATION:'负相关',MagicNum.QuotaTable.POSITIVE_RELATION:'正相关'}

class SearchQuotaDialog(ValidaDialog.ValidaDialog,object):
    def __init__(self,quota):
        self.__quota = quota
        self.__highertype = self.__quota[1]
        self.__relation = self.__quota[2]
        self.__radiolist = []
        super(SearchQuotaDialog,self).__init__("指标信息",MagicNum.ValidaDialogNum.HEADER_STATIC)
        self.setInputText(self.__quota[3:5])
        self.__radiolist[0].SetSelection(self.__highertype - MagicNum.QuotaTable.CURRENT_VALUE)
        self.__radiolist[1].SetSelection(self.__relation - MagicNum.QuotaTable.NEGATIVE_RELATION)
    
    def getTextLabel(self):
        _labelList = ["指标定义","计算公式"]
        return _labelList
    
    def getHeaderText(self):
        _text = """\
        \n 指 标 名 : """
        _text += self.__quota[0].encode('UTF-8') + "\n"
        return _text
    
    def addNewControl(self):
        _quota = ["当前指标","未来指标"]
        _ration = ["负相关","正相关"]
        self.createRadioButton(_quota,self.ButtonQuotaCmd)
        self.createRadioButton(_ration,self.ButtonRelationCmd)
         
    def createRadioButton(self,_label,_fun):
        RadioBt = wx.RadioBox(self,-1,choices = _label)
        self.__radiolist.append(RadioBt)
        self.Bind(wx.EVT_RADIOBOX, _fun, RadioBt)
        self.sizer.Add(RadioBt,0,wx.EXPAND)
    
    def ButtonQuotaCmd(self,event):
        radioSelected = event.GetEventObject()
        self.__highertype = MagicNum.QuotaTable.CURRENT_VALUE + radioSelected.GetSelection()
    
    def ButtonRelationCmd(self,event):
        radioSelected = event.GetEventObject()
        self.__relation = MagicNum.QuotaTable.NEGATIVE_RELATION + radioSelected.GetSelection()
    
    def alterQuota(self):
        _inputlist = self.getInputText()
        _db = QuotaTable.QuotaTable()
        _db.Connect()
        _db.AlterQuota("highertype", self.__highertype, self.__quota[0])
        _db.AlterQuota("relation", self.__relation, self.__quota[0])
        _db.AlterQuota("description", _inputlist[0], self.__quota[0])
        _db.AlterQuota("formula", _inputlist[1], self.__quota[0])
        _db.CloseCon()
    
    def secondButtonFun(self):
        self.alterQuota()
        self.Destroy() 
            
        
if __name__=='__main__': 
    app = wx.PySimpleApp()
    dlg = SearchQuotaDialog(['t2',MagicNum.QuotaTable.CURRENT_VALUE,MagicNum.QuotaTable.NEGATIVE_RELATION,'description','formula'])
    dlg.Run()
    app.MainLoop()