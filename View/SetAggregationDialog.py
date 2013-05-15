# -*- coding: UTF-8 -*-

import wx

CHECKBOXCOLNUM = 4
   
class SetAggregationDialog(wx.Dialog):
    def __init__(self,title,customerlist):
        self.__customerlist = customerlist
        self.__checkFlagMap = {}
        self.__checkIndexMap = {}
        
        wx.Dialog.__init__(self, None, -1, title)
        self.__topSizer = wx.BoxSizer(wx.VERTICAL)
        
        self.createStatic("输入层次数")
        self.createSpinCtrl() 
        self.createStatic("选择聚类个体") 
        self.createCheckBox() 
        self.createButton("提交")
        
        self.SetSizer(self.__topSizer)
        self.__topSizer.Fit(self)
    
    def createButton(self,label):
        _Bt = wx.Button(self,-1,label)
        self.Bind(wx.EVT_BUTTON, self.buttonCmd, _Bt)
        self.__topSizer.Add(_Bt,0,wx.ALIGN_RIGHT)
        self.__topSizer.Add(wx.StaticLine(self), 0, wx.EXPAND|wx.ALL, 5)
    
    def createStatic(self,label):
        _text = wx.StaticText(self,-1,label)
        self.__topSizer.Add(_text,0,wx.EXPAND)
        self.__topSizer.Add(wx.StaticLine(self), 0, wx.EXPAND|wx.ALL, 5)
    
    def createSpinCtrl(self):
        self.__sc = wx.SpinCtrl(self, -1,size = (100,30))
        _max = len(self.__customerlist)
        self.__sc.SetRange(1,_max)
        self.__sc.SetValue(1) 
        self.__topSizer.Add(self.__sc,0,wx.EXPAND)
        self.__topSizer.Add(wx.StaticLine(self), 0, wx.EXPAND|wx.ALL, 5)
    
    def createSingleCheckBox(self,label):
        _cb = wx.CheckBox(self,-1,label)
        self.Bind(wx.EVT_CHECKBOX,self.checkBoxCmd , _cb)
        return _cb
   
    def createCheckBox(self):
        _num = len(self.__customerlist)
        _row = _num / CHECKBOXCOLNUM + 1
        fgs = wx.GridSizer(_row,CHECKBOXCOLNUM,15,15)
        for _index,_label in enumerate(self.__customerlist):
            _cb = self.createSingleCheckBox(_label)
            self.__checkFlagMap[_cb] = False
            self.__checkIndexMap[_cb] = _index
            fgs.Add(_cb,0,0)
        
        self.__topSizer.Add(fgs,0,wx.EXPAND)
        self.__topSizer.Add(wx.StaticLine(self), 0, wx.EXPAND|wx.ALL, 5)
    
    def checkBoxCmd(self,event):
        self.__checkFlagMap[event.GetEventObject()] = not self.__checkFlagMap[event.GetEventObject()]
        
    def buttonCmd(self,event):
        self.level = self.__sc.GetValue()
        self.indexList = []
        for _ct in self.__checkFlagMap:
            if self.__checkFlagMap[_ct]:
                self.indexList.append(self.__checkIndexMap[_ct])
        self.Destroy()
    
    def Run(self):
        self.Center()
        self.ShowModal()
if __name__=='__main__': 
    app = wx.App()
    s = SetAggregationDialog("title",["afdfasfd",'bfdfd','cdfsdfafdssssssssssssf','ddfdfdsfsadfasdf','e','fdfdfd',"a",'b','c','d','e','f'])
    s.Run()
    app.MainLoop()