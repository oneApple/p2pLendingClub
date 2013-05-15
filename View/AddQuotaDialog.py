# -*- coding: UTF-8 -*-
import wx

import ValidaDialog
from GlobalData import MagicNum
from DataBase import QuotaTable


class AddQuotaDialog(ValidaDialog.ValidaDialog,object):
    def __init__(self):
        self.__highertype = MagicNum.QuotaTable.FUTURE_VALUE
        self.__relation = MagicNum.QuotaTable.NEGATIVE_RELATION
        super(AddQuotaDialog,self).__init__("添加新指标",MagicNum.ValidaDialogNum.HEADER_STATIC)       
        
    def addNewControl(self):
        _quota = ["当前指标","未来指标"]
        _ration = ["负相关","正相关"]
        self.createRadioButton(_quota,self.ButtonQuotaCmd)
        self.createRadioButton(_ration,self.ButtonRelationCmd)
         
    def createRadioButton(self,_label,_fun):
        RadioBt = wx.RadioBox(self,-1,choices = _label)
        self.Bind(wx.EVT_RADIOBOX, _fun, RadioBt)
        self.sizer.Add(RadioBt,0,wx.EXPAND)
    
    def ButtonQuotaCmd(self,event):
        radioSelected = event.GetEventObject()
        self.__highertype = MagicNum.QuotaTable.CURRENT_VALUE + radioSelected.GetSelection()
    
    def ButtonRelationCmd(self,event):
        radioSelected = event.GetEventObject()
        self.__relation = MagicNum.QuotaTable.NEGATIVE_RELATION + radioSelected.GetSelection()
    
    def getTextLabel(self):
        _labelList = ["指标名", "描述","公式"]
        return _labelList
    
    def getHeaderText(self):
        _text = """\
        \n 添 加 新 指 标
        """
        return _text
    
    def tryAgain(self,msg):
        self.Destroy()
        _dlg = AddQuotaDialog()
        _dlg.setHeaderText("\n"+msg+"\n")
        _dlg.Run()
    
    def addNewQuota(self,inputlist):
        _db = QuotaTable.QuotaTable()
        _db.Connect()
        if not _db.AddNewQuota([inputlist[0],inputlist[3],inputlist[4],inputlist[1],inputlist[2]]):
            _db.CloseCon()
            self.tryAgain("指标已存在")
            return
        print _db.SearchAllQuota()
        _db.CloseCon()
        self.Destroy()
    
    def secondButtonFun(self):
        _inputlist = self.getInputText()
        _inputlist += [self.__highertype,self.__relation]
        self.addNewQuota(_inputlist)
            
        
if __name__=='__main__': 
    app = wx.PySimpleApp()
    dlg = AddQuotaDialog()
    dlg.Run()
    app.MainLoop()