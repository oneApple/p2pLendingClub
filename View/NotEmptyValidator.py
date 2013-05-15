# -*- coding: UTF-8 -*-
import wx

class NotEmptyValidator(wx.PyValidator): # 创建验证器子类
    def __init__(self):
        wx.PyValidator.__init__(self)
 
    def Clone(self):
        """
        Note that every validator must implement the Clone() method.
        """
        return NotEmptyValidator()
 
    def Validate(self, win):#1 使用验证器方法
        textCtrl = self.GetWindow()
        text = textCtrl.GetValue()
 
        if len(text) == 0:
            wx.MessageBox("输入不能为空!", "错误")
            textCtrl.SetBackgroundColour("pink")
            textCtrl.SetFocus()
            textCtrl.Refresh()
            return False
        else:
            textCtrl.SetBackgroundColour(
            wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW))
            textCtrl.Refresh()
            return True
 
    def TransferToWindow(self):
        return True 
 
    def TransferFromWindow(self):
        return True