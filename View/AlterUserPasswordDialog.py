# -*- coding: UTF-8 -*-
import wx

import ValidaDialog
from GlobalData import MagicNum
from DataBase import UserTable


class AlterUserPasswordDialog(ValidaDialog.ValidaDialog,object):
    def __init__(self,username):
        super(AlterUserPasswordDialog,self).__init__("密码修改",MagicNum.ValidaDialogNum.HEADER_STATIC)
        self.__username = username
        
    def getTextLabel(self):
        _labelList = ["原密码","新密码","重复密码"]
        return _labelList
    
    def getHeaderText(self):
        _text = """\
        \n 修 改 密 码
        """ 
        return _text
    
    def tryAgain(self,msg):
        self.Destroy()
        _dlg = AlterUserPasswordDialog(self.__username)
        _dlg.setHeaderText("\n"+msg+"\n")
        _dlg.Run()
    
    def AlterUserPassword(self,db,psw):
        db.AlterUser("password", psw, self.__username)
        db.CloseCon()
        self.Destroy()
    
    def secondButtonFun(self):
        _inputlist = self.getInputText()
        _db = UserTable.UserTable()
        _db.Connect()
        _res = _db.SearchUser(self.__username)
        if _inputlist[0] != _res[0][1]:
            _db.CloseCon()
            self.tryAgain("密码错误")
        elif _inputlist[1] != _inputlist[2]:
            _db.CloseCon()
            self.tryAgain("密码输入不一致")
        else:
            self.AlterUserPassword(_db,_inputlist[1])
        
            
        
if __name__=='__main__': 
    app = wx.PySimpleApp()
    dlg = AlterUserPasswordDialog("keyaming")
    dlg.Run()
    app.MainLoop()