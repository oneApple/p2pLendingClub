# -*- coding: UTF-8 -*-

import wx
import NotEmptyValidator   
from GlobalData import MagicNum
   
class ValidaDialog(wx.Dialog):
    def __init__(self,title,type):
        self.__textList = []
        self.__type = type
        wx.Dialog.__init__(self, None, -1, title)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.createHeader(self.__type)
        self.createAllText()
        self.addNewControl()
        self.createButton(wx.ALIGN_CENTER)
        
        self.SetSizer(self.sizer)
        self.sizer.Fit(self)
    
    def getTextLabel(self):
        pass
    
    def getHeaderText(self):
        pass
    
    def firstButtonFun(self):
        self.Destroy()   
    
    def secondButtonFun(self):
        pass
    
    def registerButtonFun(self,event):
        pass
    
    def getInputText(self):
        _texts = []
        for _text in self.__textList:
            _texts.append(_text.GetValue())
        return _texts;
    
    def setInputText(self,textlist):
        for control,text, in zip(self.__textList,textlist):
            control.SetValue(text)
    
    def setHeaderText(self,text):
        self.__text.SetLabel(text)
        self.__text.SetForegroundColour("red")
    
    def addNewControl(self):         
        pass
    
    def createHeaderStatic(self):
        self.__text = wx.StaticText(self, -1, self.getHeaderText())
        self.__text.SetForegroundColour("green")
        self.__text.SetBackgroundColour("white")
        
        self.sizer.Add(self.__text, 0, wx.ALIGN_CENTER, 5)
        self.sizer.Add(wx.StaticLine(self), 0, wx.EXPAND|wx.ALL, 5)
    
    def createHeaderButton(self):
        jpg = wx.Image("./ico/logo.gif",wx.BITMAP_TYPE_GIF).ConvertToBitmap()
        fileButton=wx.BitmapButton(self,-1,jpg)
        self.Bind(wx.EVT_BUTTON,self.registerButtonFun,fileButton)
        self.sizer.Add(fileButton, 0, wx.EXPAND, 5)
        self.sizer.Add(wx.StaticLine(self), 0, wx.EXPAND|wx.ALL, 5)
    
    def createHeader(self,type):
        if type == MagicNum.ValidaDialogNum.HEADER_STATIC:
            self.createHeaderStatic()
        elif type == MagicNum.ValidaDialogNum.HEADER_BUTTON:
            self.createHeaderButton()
            self.createHeaderStatic()

    def createSingleText(self,sizer,label):
        _static = wx.StaticText(self, -1, label)
        _text = wx.TextCtrl(self, validator=NotEmptyValidator.NotEmptyValidator())
        sizer.Add(_static,0,wx.ALIGN_RIGHT)
        sizer.Add(_text,0,wx.EXPAND)
        self.__textList.append(_text)
    
    def createAllText(self):
        _textlist = self.getTextLabel();
        _textnum = len(_textlist)
        _fgs = wx.FlexGridSizer(_textnum, 2, 5, 10)
        for _label in _textlist:
            self.createSingleText(_fgs,_label)
        _fgs.AddGrowableCol(1)
        self.sizer.Add(_fgs, 0, wx.EXPAND|wx.ALL, 5)
    
    def createButton(self,type):
        self.sizer.Add(wx.StaticLine(self), 0, wx.EXPAND|wx.ALL, 5)
        okay   = wx.Button(self, wx.ID_OK, "提交")
        okay.SetDefault()
        cancel = wx.Button(self, wx.ID_CANCEL,"取消")
        btns = wx.StdDialogButtonSizer()
        btns.AddButton(cancel)
        btns.AddButton(okay)
        btns.Realize()
        self.sizer.Add(btns, 0, type|wx.ALL, 5)
        self.sizer.Add(wx.StaticLine(self), 0, wx.EXPAND|wx.ALL, 5)
   
    def Run(self):
        _res = self.ShowModal()
        if _res == wx.ID_OK:
            self.secondButtonFun()
        elif _res == wx.ID_CANCEL:
            self.firstButtonFun()
        #self.Destroy()
   


