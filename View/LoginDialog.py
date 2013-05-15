# -*- coding: UTF-8 -*-
import wx

import ValidaDialog
from GlobalData import MagicNum
from DataBase import UserTable
import RegisterDialog
import MainFrame

class LoginDialog(ValidaDialog.ValidaDialog,object):
    def __init__(self):
        super(LoginDialog,self).__init__("登录",MagicNum.ValidaDialogNum.HEADER_BUTTON)
    
    def getTextLabel(self):
        _labelList = ["用户名", "密码"]
        return _labelList
    
    def getHeaderText(self):
        _text = """\
        欢 迎 登 录 系 统\
        """
        return _text
    
    def tryAgain(self,msg):
        self.Destroy()
        _dlg = LoginDialog()
        _dlg.setHeaderText(msg)
        _dlg.Run()
    
    def secondButtonFun(self):
        _inputlist = self.getInputText()
        _db = UserTable.UserTable()
        _db.Connect()
        _res = _db.SearchUser(_inputlist[0])
        if not _res:
            self.tryAgain("该用户不存在")
        elif _res[0][1] != _inputlist[1]:
            self.tryAgain("密码错误")
        else:
            self.Destroy()
            MainFrame.MainFrame("综合评价",_res[0][0],_res[0][3])
        _db.CloseCon()
    
    def registerButtonFun(self,event):
        _dlg = RegisterDialog.RegisterDialog()
        self.Destroy()
        _dlg.Run()
        
        
if __name__=='__main__': 
    app = wx.PySimpleApp()
    dlg = LoginDialog()
    dlg.Run()
    app.MainLoop()