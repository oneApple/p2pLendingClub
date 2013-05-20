# -*- coding: UTF-8 -*-
import wx

from GlobalData.MagicNum import MainFramMenuId, UserDB, DataMap
from GlobalData import MagicNum
from MatrixAndGraph import DataHandle, PolyGraph, Aggregation
import AlterUserPositionDialog, AlterUserPasswordDialog, AlterUserPermissionDialog
import AddQuotaDialog, LoginDialog, SelectQuotaDialog, SetAggregationDialog
import MatrixTable


import numpy as np
import wx.grid

usermenu = {MainFramMenuId.USER_ALTERMES:"信息管理",MainFramMenuId.USER_ALTERPSW:"修改密码",MainFramMenuId.USER_LOGOUT:"注销登录"}
quotamenu = {MainFramMenuId.QUOTA_SEARCH:"指标查询",MainFramMenuId.QUOTA_ADD:"指标增加",MainFramMenuId.QUOTA_ALTER:"修改删除",
             MainFramMenuId.QUOTA_COMMENT:"指标评论",MainFramMenuId.COMMENT_SEARCH:"查看评论"}
evaluatemenu = {MainFramMenuId.EVALUATE_GETDATA:"数据输入",MainFramMenuId.EVALUATE_COMPUTE:"数据处理",
                MainFramMenuId.GRAYRE_TOTAL:"客户群价值",MainFramMenuId.GRAYRE_SEPARATE:"当前和未来"}
aggregatmenu = {MainFramMenuId.AGGREGAT_CHOSEELM:"个体选择",MainFramMenuId.AGGREGAT_AGGGRAPH:"聚类分析",
                MainFramMenuId.AGGREGAT_CHOSELEV:"层次选择",MainFramMenuId.AGGREGAT_CLASSIFY:"类别分析"}
systemmenu = {MainFramMenuId.SYSTEM_AUDIT:"用户审核",MainFramMenuId.SYSTEM_PERMISSION:"权限管理",
              MainFramMenuId.SYSTEM_HELP:"使用帮助",MainFramMenuId.SYSTEM_REBUILDDB:"清空数据"}

menulabel = ("用户管理","指标管理","灰色关联分析","聚类分析","系统管理")
menuchild = (usermenu,quotamenu,evaluatemenu,aggregatmenu,systemmenu)

rootquota = []
adminquota = [MainFramMenuId.SYSTEM_PERMISSION]
normalquota = adminquota + [MainFramMenuId.SYSTEM_AUDIT,MainFramMenuId.QUOTA_ADD,MainFramMenuId.QUOTA_ALTER]
nothingquota = normalquota + [MainFramMenuId.EVALUATE_COMPUTE,MainFramMenuId.EVALUATE_GETDATA,MainFramMenuId.QUOTA_COMMENT,
                              MainFramMenuId.GRAYRE_SEPARATE,MainFramMenuId.GRAYRE_TOTAL,MainFramMenuId.AGGREGAT_AGGGRAPH,
                              MainFramMenuId.AGGREGAT_CHOSEELM,MainFramMenuId.AGGREGAT_CHOSELEV,MainFramMenuId.AGGREGAT_CLASSIFY]

menudisable = {UserDB.PERMISSION_NOTHING:nothingquota,UserDB.PERMISSION_NORMAL:normalquota,UserDB.PERMISSION_ADMIN:adminquota,UserDB.PERMISSION_ROOT:rootquota}

class MainFrame(wx.Frame):
    def __init__(self,title,username,permission):
        wx.Frame.__init__(self,None,-1,title,size = (1280,900))
        self.__username = username
        self.__permission = permission
        self.__data = DataHandle.DataHandle()
        self.__level = 3
        self.__indexlist = []
        
        self.__vbox_top = wx.BoxSizer(wx.VERTICAL)
        self.__panel_top = wx.Panel(self)
        
        self.createMenuBar()
        self.disableMenu()
        self.createButton()
        self.createMatrixTabel()
        
        self.__panel_top.SetSizer(self.__vbox_top)
        self.Center()
        self.Show()
        
    def createSingleButton(self,panel,vbox,label,fun):
        _button = wx.Button(panel,-1,label)
        vbox.Add(_button,wx.EXPAND)
        self.Bind(wx.EVT_BUTTON,fun ,_button)
    
    def createButton(self):
        panel = wx.Panel(self.__panel_top,-1)
        vbox = wx.BoxSizer(wx.HORIZONTAL)
        
        _btmap = {"原始数据":self.buttonOriginalCmd,"标准化数据":self.buttonStandardCmd,
                  "灰色关联系数":self.buttonGrayRelationCoefficientCmd,
                  "指标权重":self.buttonQuotaWeightCmd,"灰色关联度":self.buttonGrayRelationCmd,
                  }
        _labellist = ["原始数据","标准化数据","灰色关联系数","指标权重","灰色关联度"]
        for _label in _labellist:
            self.createSingleButton(panel, vbox, _label, _btmap[_label])
        
        panel.SetSizer(vbox)
        self.__vbox_top.Add(panel,0,wx.EXPAND)
        self.__vbox_top.Add(wx.StaticLine(self.__panel_top), 0, wx.EXPAND|wx.ALL, 5)
        self.__vbox_top.Add(wx.StaticLine(self.__panel_top), 0, wx.EXPAND|wx.ALL, 5)
    
    def changeGrid(self,type,trans = True,rowlabel = None,collabel = None):
        try:
            if not collabel:
                collabel = self.__data.GetData(DataMap.ZERO_ROWLABEL)
            if not rowlabel:
                rowlabel = self.__collabel
            _matrix = np.array(self.__data.GetData(type))
            if trans:
                _matrix = np.swapaxes(_matrix,0,1)
            _m = MatrixTable.MatrixTable(_matrix,rowlabel,collabel)
            self.__grid.ClearGrid()#清空表格
            self.__grid.SetTable(_m)
            self.__grid.Hide()
            self.__grid.Show()
        except (AttributeError,UnboundLocalError),e:
            wx.MessageBox("请先输入并计算","错误",wx.ICON_ERROR|wx.YES_DEFAULT)
    
    def buttonOriginalCmd(self,event):
        self.changeGrid(DataMap.ONE_ORIGINAL)
    
    def buttonStandardCmd(self,event):
        self.changeGrid(DataMap.TWO_STANDARD)
    
    def buttonGrayRelationCoefficientCmd(self,event):
        self.changeGrid(DataMap.THREE_GRCOEFFICIENT)
    
    def buttonQuotaWeightCmd(self,event):
        _collabel = ["标准差","平均值","变异系数","权重"]
        self.changeGrid(DataMap.FOUR_QUOTAWEIGHT,False,collabel = _collabel)
    
    def buttonGrayRelationCmd(self,event):
        _collabel = ["客户群价值","客户群价值排序","当前价值","当前价值排序","未来价值","未来价值排序"]
        self.changeGrid(DataMap.FIVE_GRWEIGHT,False,self.__data.GetData(DataMap.ZERO_ROWLABEL),_collabel)
    
    def createMatrixTabel(self):
        self.__gridPanel = wx.Panel(self.__panel_top,-1)
        vbox = wx.BoxSizer(wx.HORIZONTAL)
        self.__grid = wx.grid.Grid(self.__gridPanel)
        table = MatrixTable.MatrixTable([""] * 25,[""] * 20,[""] * 25)
        self.__grid.SetTable(table, True)
        self.__grid.SetRowLabelSize(150)
        vbox.Add(self.__grid,wx.EXPAND)
        self.__gridPanel.SetSizer(vbox)
        self.__vbox_top.Add(self.__gridPanel,0,wx.EXPAND)
    
    def createMenuBar(self):
        self.__menuBar = wx.MenuBar()
        for _index,_childmenu in enumerate(menuchild):
            self.createMenu(menulabel[_index],_childmenu)
        self.setMenuEvent()
        self.SetMenuBar(self.__menuBar)
    
    def createMenu(self,label,child):
        _menu = wx.Menu()
        for _menuid in child:
            _menu.Append(_menuid,child[_menuid])
            _menu.AppendSeparator()
        self.__menuBar.Append(_menu,label)
    
    def disableMenu(self):
        _menulist = menudisable[self.__permission]
        for menu in _menulist:
            wx.MenuBar.Enable(self.__menuBar,menu,False)
    
    def setMenuEvent(self):
        wx.EVT_MENU(self,MainFramMenuId.USER_ALTERMES,self.menuAlterUserPosCmd);
        wx.EVT_MENU(self,MainFramMenuId.USER_ALTERPSW,self.menuAlterUserPswCmd);
        wx.EVT_MENU(self,MainFramMenuId.USER_LOGOUT,self.menuLogoutCmd);
        
        wx.EVT_MENU(self,MainFramMenuId.SYSTEM_PERMISSION,self.menuAlterUserPerCmd)
        wx.EVT_MENU(self,MainFramMenuId.SYSTEM_AUDIT,self.menuAllowUserPerCmd)
        wx.EVT_MENU(self,MainFramMenuId.SYSTEM_HELP,self.menuHelpCmd)
        wx.EVT_MENU(self,MainFramMenuId.SYSTEM_REBUILDDB,self.menuRebuildDbCmd)
        
        wx.EVT_MENU(self,MainFramMenuId.QUOTA_ADD,self.menuAddQuotaCmd)
        wx.EVT_MENU(self,MainFramMenuId.QUOTA_ALTER,self.menuManageQuotaCmd)
        wx.EVT_MENU(self,MainFramMenuId.QUOTA_COMMENT,self.menuAddCommentCmd)
        wx.EVT_MENU(self,MainFramMenuId.COMMENT_SEARCH,self.menuSearchCommentCmd)
        wx.EVT_MENU(self,MainFramMenuId.QUOTA_SEARCH,self.menuSearchQuotaCmd)
        
        wx.EVT_MENU(self,MainFramMenuId.EVALUATE_GETDATA,self.menuGetDataCmd)
        wx.EVT_MENU(self,MainFramMenuId.EVALUATE_COMPUTE,self.menuComputeCmd)
        
        wx.EVT_MENU(self,MainFramMenuId.AGGREGAT_CHOSEELM,self.menuChoseAggreElemCmd)
        wx.EVT_MENU(self,MainFramMenuId.AGGREGAT_AGGGRAPH,self.menuWardGarphCmd)
        wx.EVT_MENU(self,MainFramMenuId.AGGREGAT_CHOSELEV,self.menuChoseLevelCmd)
        wx.EVT_MENU(self,MainFramMenuId.AGGREGAT_CLASSIFY,self.menuAggregationCmd)
        
        wx.EVT_MENU(self,MainFramMenuId.GRAYRE_SEPARATE,self.menuSeparateGrapyCmd)
        wx.EVT_MENU(self,MainFramMenuId.GRAYRE_TOTAL,self.menuTotalGrapyCmd)
    
    def rebuildDb(self,db):
        db.Connect()
        db.DeleteTable()
        db.CreateTable()
        db.CloseCon()
    
    def menuRebuildDbCmd(self,event):
        from DataBase import CommentTable, QuotaTable, UserTable
        _dblist = [CommentTable.CommentTable(),QuotaTable.QuotaTable(),UserTable.UserTable()]
        for _db in _dblist:
            self.rebuildDb(_db)
    
    def menuAggregationCmd(self,event):
        try:
            self.__data.ComputeAggregationResult(self.__level)
            _collabel = ["客户群价值","当前价值","未来价值","客户群组成"]
            self.changeGrid(DataMap.SEVEN_AGGREGATION,False,[x for x in range(self.__level)],_collabel)
        except:
            wx.MessageBox("数据获取错误","错误",wx.ICON_ERROR|wx.YES_DEFAULT)
    
    def menuChoseLevelCmd(self,event):
        try:
            s = SetAggregationDialog.SetAggregationDialog("聚类设置",self.__customerlist,MagicNum.SetAggregationDialog.AGGREGAT_SETLEVEL)
            s.Run()
            self.__level = s.level
        except:
            wx.MessageBox("请先获取数据","错误",wx.ICON_ERROR|wx.YES_DEFAULT)

    def menuChoseAggreElemCmd(self,event):
        try:
            s = SetAggregationDialog.SetAggregationDialog("聚类设置",self.__customerlist,MagicNum.SetAggregationDialog.AGGREGAT_CHOSEELM)
            s.Run()
            self.__indexlist = s.indexList
        except:
            wx.MessageBox("请先获取数据","错误",wx.ICON_ERROR|wx.YES_DEFAULT)
    
    def menuAlterUserPosCmd(self,event):
        _dlg = AlterUserPositionDialog.AlterUserPositionDialog(self.__username)
        _dlg.Run()
    
    def menuAlterUserPswCmd(self,event):
        _dlg = AlterUserPasswordDialog.AlterUserPasswordDialog(self.__username)
        _dlg.Run()
    
    def menuLogoutCmd(self,event):
        self.Destroy()
        _dlg = LoginDialog.LoginDialog()
        _dlg.Run()
    
    def menuAlterUserPerCmd(self,event):
        _dlg = AlterUserPermissionDialog.AlterUserPermissionDialog("提升权限",UserDB.PERMISSION_NORMAL)
        _dlg.Run()
    
    def menuAddQuotaCmd(self,event):
        _dlg = AddQuotaDialog.AddQuotaDialog()
        _dlg.Run()
    
    def menuSearchCommentCmd(self,event):
        from DataBase import CommentTable
        try:
            _db = CommentTable.CommentTable()
            _db.Connect()
            _res = _db.SearchAllComment()
            _db.CloseCon()
            collabel = ["指标名","用户名","评论","评分"]
            rowlabel = []
            for index in range(len(_res)):
                rowlabel.append(index)
            _matrix = np.array(_res)
            _m = MatrixTable.MatrixTable(_matrix,collabel,rowlabel)
            self.__grid.ClearGrid()#清空表格
            self.__grid.SetTable(_m)
            self.__grid.Hide()
            self.__grid.Show()
        except (AttributeError,UnboundLocalError),e:
            wx.MessageBox("数据获取错误","错误",wx.ICON_ERROR|wx.YES_DEFAULT)
    
    def menuSearchQuotaCmd(self,event):
        def transindex2label(list):
            templist = []
            templist.append(list[0])
            if list[1] - MagicNum.QuotaTable.CURRENT_VALUE:
                templist.append("未来指标".decode('utf8'))
            else:
                templist.append("当前价值".decode('utf8'))
            if list[2] - MagicNum.QuotaTable.NEGATIVE_RELATION:
                templist.append("正相关".decode('utf8'))
            else:
                templist.append("负相关".decode('utf8'))
            templist.append(list[3])
            templist.append(list[4])
            return templist
        
        from DataBase import QuotaTable
        try:
            _db = QuotaTable.QuotaTable()
            _db.Connect()
            _res = _db.SearchAllQuota()
            _db.CloseCon()
            collabel = ["指标名","指标类型","相关性","描述","公式"]
            rowlabel = []
            for index in range(len(_res)):
                rowlabel.append(index)
            
            tempmatrix = []
            for _list in _res:    
                tempmatrix.append(transindex2label(_list))
            _matrix = np.array(tempmatrix)
            
            _m = MatrixTable.MatrixTable(_matrix,collabel,rowlabel)
            self.__grid.ClearGrid()#清空表格
            self.__grid.SetTable(_m)
            self.__grid.Hide()
            self.__grid.Show()
        except (AttributeError,UnboundLocalError),e:
            wx.MessageBox("数据获取错误","错误",wx.ICON_ERROR|wx.YES_DEFAULT)

    def menuManageQuotaCmd(self,event):
        _dlg = SelectQuotaDialog.SelectQuotaDialog("指标管理",self.__username,MagicNum.SelectQuotaDialog.DELETEANDALTER)
        _dlg.Run()
    
    def menuAddCommentCmd(self,event):
        _dlg = SelectQuotaDialog.SelectQuotaDialog("指标评论",self.__username,MagicNum.SelectQuotaDialog.ADDCOMMENT)
        _dlg.Run()
    
    def menuGetDataCmd(self,event):
        dlg = wx.FileDialog(None,
                            message="请选择一个文件",
                            wildcard="*.plc" ,
                            style=wx.OPEN
                            )
        if dlg.ShowModal() == wx.ID_OK:
            self.__customerlist = self.__data.GetFileData(dlg.GetPath())
        dlg.Destroy()
    
    def menuComputeCmd(self,event):
        self.__collabel = []
        self.__optlist = []
        from DataBase import QuotaTable
        _db = QuotaTable.QuotaTable()
        _db.Connect()
        _res = _db.SearchAllQuota()
        _db.CloseCon()
        _curlist = []
        _futlist = []
        _index = 0
        for single in _res:
            if single[1] == MagicNum.QuotaTable.CURRENT_VALUE:
                _curlist.append(_index)
            elif single[1] == MagicNum.QuotaTable.FUTURE_VALUE:
                _futlist.append(_index)
            _index += 1
            self.__collabel.append(single[0])
            self.__optlist.append(single[2])
        try:
            self.__indexlist.sort()
            print self.__indexlist
            self.__data.ComputeGrayRelationResult(self.__optlist,_curlist,_futlist)
        except Exception,e:
            print e 
            wx.MessageBox("请先获取数据","错误",wx.ICON_ERROR|wx.YES_DEFAULT)
    
    def menuAllowUserPerCmd(self,event):
        _dlg = AlterUserPermissionDialog.AlterUserPermissionDialog("审核用户",UserDB.PERMISSION_NOTHING)
        _dlg.Run()
    
    def menuHelpCmd(self,event):
        _dlg = wx.MessageDialog(self,"copy@kao","使用帮助",wx.OK|wx.ICON_INFORMATION)
        _dlg.ShowModal()
        _dlg.Destroy()
    
    def closewindow(self,event):
        self.Destroy() 
    
    def menuTotalGrapyCmd(self,event):
        "此处是客户群价值图"
        try:
            ylist = np.arange(0,1,0.1)
            p = PolyGraph.PolyGraph(self.__data.GetData(DataMap.ZERO_ROWLABEL),ylist,self.__data.GetData(DataMap.FIVE_GRWEIGHT))
            #以下四个值分别为标题，ｙ轴标题，ｘ轴标题，折线标签
            p.Draw("Customer Group Value Gray Relation", "Customer", "Gray Relation",["customer value"])
        except (AttributeError,UnboundLocalError),e:
            wx.MessageBox("数据获取错误","错误",wx.ICON_ERROR|wx.YES_DEFAULT)

    def menuSeparateGrapyCmd(self,event):
        "此处是当前未来价值图"
        try:
            ylist = np.arange(0,1,0.1)
            p = PolyGraph.PolyGraph(self.__data.GetData(DataMap.ZERO_ROWLABEL),ylist,[self.__data.GetData(DataMap.FIVE_GRWEIGHT)[2],self.__data.GetData(DataMap.FIVE_GRWEIGHT)[4]])
            #以下四个值分别为标题，ｙ轴标题，ｘ轴标题，折线标签
            p.Draw("Customer Group Value Gray Relation", "Customer", "Gray Relation",["current","future"])
        except (AttributeError,UnboundLocalError),e:
            wx.MessageBox("数据获取错误","错误",wx.ICON_ERROR|wx.YES_DEFAULT)
            
    def menuWardGarphCmd(self,event):
        "此处是聚类图"
        xlabel = self.__data.ComputeLinkResult(self.__indexlist)
        a = Aggregation.Aggregation(self.__data.GetData(MagicNum.DataMap.SIX_LINKRESULT),
                                    xlabel)
                                    #self.__data.GetData(MagicNum.DataMap.ZERO_ROWLABEL))
        #三个值分别为标题，ｙ轴标题，ｘ轴标题
        a.Draw("Ward Aggregation", "Customer", "Value")
        
if __name__=='__main__': 
    app = wx.App()
    f = MainFrame("在线客户群价值评价系统","keyaming",2003)
    app.MainLoop()
    