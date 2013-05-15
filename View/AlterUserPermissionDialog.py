# -*- coding: UTF-8 -*-

import wx
from DataBase import UserTable
from GlobalData import MagicNum
   
class AlterUserPermissionDialog(wx.SingleChoiceDialog):
    def __init__(self,title,type):
        self.__type = type
        self.__userlist = self.getUserList(type)
        super(AlterUserPermissionDialog,self).__init__(None,"选择用户",title,self.__userlist)
   
    def getUserList(self,type):
        _db = UserTable.UserTable()
        _db.Connect()
        _sql = "select name from UserDB where permission=?"
        _res = _db.Search(_sql,[type])
        _db.CloseCon()
        _userlist = []
        for name in _res:
            _userlist.append(name[0])
        return _userlist
   
    def secondButtonFun(self):
        _choice = self.GetStringSelection()
        _db = UserTable.UserTable()
        _db.Connect()
        _db.AlterUser("permission", self.__type + 1, _choice)
        _db.CloseCon()
        
    def firstButtonFun(self):
        pass 
   
    def Run(self):
        _res = self.ShowModal()
        if _res == wx.ID_OK:
            self.secondButtonFun()
        elif _res == wx.ID_CANCEL:
            self.firstButtonFun()
        self.Destroy()
   
if __name__=='__main__': 
    app = wx.App()
    f = AlterUserPermissionDialog("修改权限",MagicNum.UserDB.PERMISSION_NORMAL)
    f.Run()
    app.MainLoop()
