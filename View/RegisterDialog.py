# -*- coding: UTF-8 -*-
import wx

import ValidaDialog
import MainFrame
from GlobalData import MagicNum
from DataBase import UserTable


class RegisterDialog(ValidaDialog.ValidaDialog,object):
    def __init__(self):
        super(RegisterDialog,self).__init__("注册",MagicNum.ValidaDialogNum.HEADER_STATIC)
    
    def getTextLabel(self):
        _labelList = ["用户名", "职位","密码","重复密码"]
        return _labelList
    
    def getHeaderText(self):
        _text = """\
        \n 欢 迎 注 册 系 统
        """
        return _text
    
    def tryAgain(self,msg):
        self.Destroy()
        _dlg = RegisterDialog()
        _dlg.setHeaderText("\n"+msg+"\n")
        _dlg.Run()
    
    def addNewUser(self,inputlist):
        _db = UserTable.UserTable()
        _db.Connect()
        if not _db.AddNewUser([inputlist[0],inputlist[2],inputlist[1]]):
            self.tryAgain("用户已存在")
            _db.CloseCon()
            return
        _db.CloseCon()
        self.Destroy()
        MainFrame.MainFrame("综合评价",inputlist[0],MagicNum.UserDB.PERMISSION_NOTHING)
    
    def secondButtonFun(self):
        _inputlist = self.getInputText()
        if _inputlist[2] != _inputlist[3]:
            self.tryAgain("密码输入不一致")
        else:
            self.addNewUser(_inputlist)
            
        
if __name__=='__main__': 
    app = wx.PySimpleApp()
    dlg = RegisterDialog()
    dlg.Run()
    app.MainLoop()