# -*- coding: UTF-8 -*-

import wx

from DataBase import QuotaTable ,CommentTable
import SearchQuotaDialog
   
class SelectQuotaDialog(wx.Dialog):
    def __init__(self,title,username,flag):
        
        self.__username = username
        wx.Dialog.__init__(self, None, -1, title)
        
        self.__topSizer = wx.BoxSizer(wx.VERTICAL)
        
        self.createStatic()
        self.createComboBox()
        
        from GlobalData import MagicNum
        if flag == MagicNum.SelectQuotaDialog.DELETEANDALTER:
            self.createDeleAndSearButton()
        elif flag == MagicNum.SelectQuotaDialog.ADDCOMMENT:
            self.createCommentText()
            self.createCommentButton()
        
        self.SetSizer(self.__topSizer)
        self.__topSizer.Fit(self)
   
    def createStatic(self):
        self.__text = wx.StaticText(self, -1, "\n请 选 择 指 标")
        self.__text.SetForegroundColour("green")
        self.__text.SetBackgroundColour("white")
        
        self.__topSizer.Add(self.__text, 0, wx.ALIGN_CENTER, 5)
        self.__topSizer.Add(wx.StaticLine(self), 0, wx.EXPAND|wx.ALL, 5)
   
    def createComboBox(self):
        _db = QuotaTable.QuotaTable()
        _db.Connect()
        self.__res = _db.SearchAllQuota()
        _db.CloseCon()
        _quotaList = []
        for quota in self.__res:
            _quotaList.append(quota[0])
        self.__combo = wx.ComboBox(self, -1, _quotaList[0], choices = _quotaList, size = (300,30),style = wx.CB_DROPDOWN)
        self.__combo.SetSelection(0)
        self.__topSizer.Add(self.__combo, 0, wx.ALIGN_CENTER, 5)
        self.__topSizer.Add(wx.StaticLine(self), 0, wx.EXPAND|wx.ALL, 5)
    
    def createDeleAndSearButton(self):
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        
        deleteBt = wx.Button(self,-1,"删除")
        self.Bind(wx.EVT_BUTTON, self.buttonDeleteCmd, deleteBt)
        searchBt = wx.Button(self,-1,"修改")
        self.Bind(wx.EVT_BUTTON, self.buttonSearchCmd, searchBt)
        
        hsizer.Add(deleteBt, 0, wx.ALIGN_TOP, 10)
        hsizer.Add(searchBt, 0, wx.ALIGN_TOP, 10)
        
        self.__topSizer.Add(hsizer,0,wx.ALIGN_RIGHT)
        self.__topSizer.Add(wx.StaticLine(self), 0, wx.EXPAND|wx.ALL, 5)
    
    def createCommentText(self):
        self.__commentText = wx.TextCtrl(self, -1,
                  "您可以在这里写下对该指标的评论\n"
                  "在下面选择该指标的分数,分数越高表示改指标越重要",
                  size=(250, 100), style=wx.TE_MULTILINE) #创建一个文本控件
        self.__commentText.SetInsertionPoint(0) #设置插入点

        self.__topSizer.Add(self.__commentText,0,wx.EXPAND)
        self.__topSizer.Add(wx.StaticLine(self), 0, wx.EXPAND|wx.ALL, 5)
    
    def createCommentButton(self):
        self.__sc = wx.SpinCtrl(self, -1,size = (100,30))
        self.__sc.SetRange(1,7)
        self.__sc.SetValue(4)
        
        commentBt = wx.Button(self,-1,"评论")
        self.Bind(wx.EVT_BUTTON, self.buttonCommentCmd, commentBt)

        self.__topSizer.Add(self.__sc,0,wx.ALIGN_LEFT)
        self.__topSizer.Add(commentBt,0,wx.ALIGN_RIGHT)
        self.__topSizer.Add(wx.StaticLine(self), 0, wx.EXPAND|wx.ALL, 5)
        
    def buttonSearchCmd(self,event):
        _index = self.__combo.GetSelection()
        #self.Destroy()
        _db = QuotaTable.QuotaTable()
        _db.Connect()
        self.__res = _db.SearchAllQuota()
        _db.CloseCon()
        _dlg = SearchQuotaDialog.SearchQuotaDialog(self.__res[_index])
        _dlg.Run()
        
    def buttonDeleteCmd(self,event):
        _index = self.__combo.GetSelection()
        _db = QuotaTable.QuotaTable()
        _db.Connect()
        _db.DeleteQuota(self.__res[_index][0])
        _db.CloseCon()
        del self.__res[_index]
        self.Destroy()
        _dlg = SelectQuotaDialog("指标管理",self.__username)
        _dlg.Run()
        
    def buttonCommentCmd(self,event):
        _index = self.__combo.GetSelection()
        _db = CommentTable.CommentTable()
        _db.Connect()
        _db.AddNewComment([self.__res[_index][0],self.__username,self.__commentText.GetValue(),self.__sc.GetValue()])
        _db.CloseCon()
        
    
    def Run(self):
        _res = self.ShowModal()
   
if __name__=='__main__': 
    app = wx.App()
    s = SelectQuotaDialog("指标管理","keyaming")
    s.Run()
    app.MainLoop()
