import wx

from View import LoginDialog

app = wx.PySimpleApp()
dlg = LoginDialog.LoginDialog()
dlg.Run()
app.MainLoop()