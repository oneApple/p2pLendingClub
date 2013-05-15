# -*- coding: UTF-8 -*-
import wx

import ValidaDialog
from GlobalData import MagicNum
from DataBase import UserTable


class AlterUserPositionDialog(ValidaDialog.ValidaDialog,object):
    def __init__(self,username):
        super(AlterUserPositionDialog,self).__init__("职位修改",MagicNum.ValidaDialogNum.HEADER_STATIC)
        self.__username = username
        
    def getTextLabel(self):
        _labelList = ["职位","密码"]
        return _labelList
    
    def getHeaderText(self):
        _text = """\
        \n 修 改 职 位
        """ 
        return _text
    
    def tryAgain(self,msg):
        self.Destroy()
        _dlg = AlterUserPositionDialog(self.__username)
        _dlg.setHeaderText("\n"+msg+"\n")
        _dlg.Run()
    
    def AlterUserPosition(self,db,pos):
        db.AlterUser("position", pos, self.__username)
        db.CloseCon()
        self.Destroy()
    
    def secondButtonFun(self):
        _inputlist = self.getInputText()
        _db = UserTable.UserTable()
        _db.Connect()
        _res = _db.SearchUser(self.__username)
        if _inputlist[1] != _res[0][1]:
            _db.CloseCon()
            self.tryAgain("密码错误")
        else:
            self.AlterUserPosition(_db,_inputlist[0])
        
            
        
if __name__=='__main__': 
    app = wx.PySimpleApp()
    dlg = AlterUserPositionDialog("keyaming")
    dlg.Run()
    app.MainLoop()