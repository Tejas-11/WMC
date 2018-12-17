#this is a fully functional GUI but to optimize
#we can merge AddPanel and EditPanel into a single UpdatePanel
#since most of what they do is the same
import wx,csv,os

class ListPanel(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self,parent=parent)
        self.makeList()
        self.makeButt()
    def makeList(self):
        self.llist=wx.ListCtrl(self,wx.ID_ANY,pos=(50,50), size=(430,300), style=wx.LC_REPORT|wx.BORDER_SUNKEN)
        self.llist.InsertColumn(0,'No.')
        self.llist.SetColumnWidth(0, 40)
        self.llist.InsertColumn(1,'Name')
        self.llist.SetColumnWidth(1, 200)
        self.llist.InsertColumn(2,'Chapter No.', wx.LIST_FORMAT_RIGHT)
        self.llist.InsertColumn(3,'Type')
        self.reload()
    def reload(self):
        self.llist.DeleteAllItems()
        self.getAist()
        self.fillAist()
    def getAist(self):
        self.aist=[]
        with open('aist.csv', newline='') as f:  
            reader = csv.reader(f,delimiter=',')
            for row in reader:
                self.aist.append(row)
            self.aist.pop(0)
    def fillAist(self):
        index=0
        for ele in self.aist:
            stid=str(index+1)
            self.llist.InsertItem(index,stid)
            self.llist.SetItem(index,1,ele[0])
            self.llist.SetItem(index,2,ele[2])
            self.llist.SetItem(index,3,ele[3])
            index+=1
    def makeButt(self):
        xx=530
        yy=80
        dd=60
        self.AddButt=wx.Button(self,pos=(xx,yy),label="Add",size=(90, 30))
        self.EdButt=wx.Button(self,pos=(xx,yy+dd),label="Edit",size=(90, 30))
        self.DetButt=wx.Button(self,pos=(xx,yy+2*dd),label="Details",size=(90, 30))
        self.DelButt=wx.Button(self,pos=(xx,yy+3*dd),label="Delete",size=(90, 30))
        #bind button handlers
        self.DelButt.Bind(wx.EVT_BUTTON,self.OnDelete)
    def OnDelete(self,event):
        i=self.llist.GetSelectedItemCount()
        if i==1:
            dlg=wx.MessageDialog(self,'Are you sure you want to delete the selected item?','Warning!',wx.YES_NO|wx.CENTRE|wx.STAY_ON_TOP)
            val=dlg.ShowModal()
            if val==wx.ID_YES:
                i=int(self.llist.GetFirstSelected())
                fl=[]
                with open('aist.csv', newline='') as f:  
                    reader = csv.reader(f,delimiter=',')
                    ix=0
                    for row in reader:
                        if ix==(i+1):
                            ix+=1
                            continue
                        fl.append(row)
                        ix+=1
                with open('aist.csv', 'w',newline='') as f:  
                    writer = csv.writer(f,delimiter=',')
                    for row in fl:
                        writer.writerow(row)
                self.reload()
        else:
            dlg = wx.MessageDialog(self, 'Please select exactly one item from the list to delete','Warning!', wx.OK|wx.ICON_ERROR|wx.CENTRE|wx.STAY_ON_TOP)
            dlg.ShowModal()

class AddPanel(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self,parent=parent)
        self.makeForm()
        self.addButts()
    def addButts(self):
        self.adbut=wx.Button(self,pos=(250,300),label="Add",size=(90, 30))
        self.babut=wx.Button(self,pos=(120,300),label="GoBack",size=(90, 30))
    def makeForm(self):
        self.naxt=wx.StaticText(self, wx.ID_ANY, label="Name:", pos=(80,60),
           size=(40,20), style=0)
        self.inxt=wx.StaticText(self, wx.ID_ANY, label="Chapter Number:", pos=(20,120),
           size=(100,20), style=0)
        self.tyxt=wx.StaticText(self, wx.ID_ANY, label="Type:", pos=(80,180),
           size=(40,20), style=0)
        self.urxt=wx.StaticText(self, wx.ID_ANY, label="Url:", pos=(90,240),
           size=(30,20), style=0)
        self.name=wx.TextCtrl(self,pos=(120,60),size=(200,20))
        self.chIn=wx.TextCtrl(self,pos=(120,120),size=(90,20))
        self.btype=wx.TextCtrl(self,pos=(120,180),size=(90,20))
        self.url=wx.TextCtrl(self,pos=(120,240),size=(450,20))
    def clearForm(self):
        self.name.SetValue('')
        self.chIn.SetValue('')
        self.url.SetValue('')
        self.btype.SetValue('')

class EditPanel(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self,parent=parent)
        self.makeForm()
        self.addButts()
    def addButts(self):
        self.edbut=wx.Button(self,pos=(250,300),label="Edit",size=(90, 30))
        self.babut=wx.Button(self,pos=(120,300),label="GoBack",size=(90, 30))
    def makeForm(self):
        self.naxt=wx.StaticText(self, wx.ID_ANY, label="Name:", pos=(80,60),
           size=(40,20), style=0)
        self.inxt=wx.StaticText(self, wx.ID_ANY, label="Chapter Number:", pos=(20,120),
           size=(100,20), style=0)
        self.tyxt=wx.StaticText(self, wx.ID_ANY, label="Type:", pos=(80,180),
           size=(40,20), style=0)
        self.urxt=wx.StaticText(self, wx.ID_ANY, label="Url:", pos=(90,240),
           size=(30,20), style=0)
        self.name=wx.TextCtrl(self,pos=(120,60),size=(200,20))
        self.chIn=wx.TextCtrl(self,pos=(120,120),size=(90,20))
        self.btype=wx.TextCtrl(self,pos=(120,180),size=(90,20))
        self.url=wx.TextCtrl(self,pos=(120,240),size=(450,20))
    def fillForm(self,nm,chn,uri,tp):
        self.name.SetValue(nm)
        self.chIn.SetValue(chn)
        self.url.SetValue(uri)
        self.btype.SetValue(tp)

class DetPanel(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self,parent=parent)
        self.makeForm()
        self.addButts()
    def addButts(self):
        self.babut=wx.Button(self,pos=(120,300),label="GoBack",size=(90, 30))
    def makeForm(self):
        self.naxt=wx.StaticText(self, wx.ID_ANY, label="Name:", pos=(80,60),
           size=(40,20), style=0)
        self.inxt=wx.StaticText(self, wx.ID_ANY, label="Chapter Number:", pos=(20,120),
           size=(100,20), style=0)
        self.tyxt=wx.StaticText(self, wx.ID_ANY, label="Type:", pos=(80,180),
           size=(40,20), style=0)
        self.urxt=wx.StaticText(self, wx.ID_ANY, label="Url:", pos=(90,240),
           size=(30,20), style=0)
        self.name=wx.TextCtrl(self,pos=(120,60),size=(200,20))
        self.chIn=wx.TextCtrl(self,pos=(120,120),size=(90,20))
        self.btype=wx.TextCtrl(self,pos=(120,180),size=(90,20))
        self.url=wx.TextCtrl(self,pos=(120,240),size=(450,20))
    def fillForm(self,nm,chn,uri,tp):
        self.name.SetValue(nm)
        self.chIn.SetValue(chn)
        self.url.SetValue(uri)
        self.btype.SetValue(tp)

class MainWindow(wx.Frame):
    def __init__(self,parent,title):
        wx.Frame.__init__(self,parent,title=title,size=(750,500))
        self.initMenu()
        self.LP=ListPanel(self)
        self.AP=AddPanel(self)
        self.DP=DetPanel(self)
        self.EP=EditPanel(self)
        self.AP.Hide()
        self.DP.Hide()
        self.EP.Hide()
        #do sizer stuff
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.AP, 1, wx.EXPAND)
        self.sizer.Add(self.LP, 1, wx.EXPAND)
        self.sizer.Add(self.DP, 1, wx.EXPAND)
        self.sizer.Add(self.EP, 1, wx.EXPAND)
        self.SetSizer(self.sizer)
        #bind switch panel events
        self.LP.AddButt.Bind(wx.EVT_BUTTON,self.OnAdd)
        self.LP.EdButt.Bind(wx.EVT_BUTTON,self.OnEdit)
        self.LP.DetButt.Bind(wx.EVT_BUTTON,self.OnDetails)
        #bind all go back events
        self.AP.babut.Bind(wx.EVT_BUTTON,self.OnGoBack)
        self.DP.babut.Bind(wx.EVT_BUTTON,self.OnGoBack)
        self.EP.babut.Bind(wx.EVT_BUTTON,self.OnGoBack)
        #bind all change aist events
        self.AP.adbut.Bind(wx.EVT_BUTTON,self.OnAddData)
        self.EP.edbut.Bind(wx.EVT_BUTTON,self.OnEditData)
        self.Show(True)
    def initMenu(self):
        self.CreateStatusBar()
        #create menu
        filemenu=wx.Menu()
        menuAdd=filemenu.Append(wx.ID_ANY,"&Add","Add another comic,manga or webtoon to the list")
        filemenu.AppendSeparator()
        menuAbout=filemenu.Append(wx.ID_ABOUT,"&About","WMC downloads and store comics,webtoons and manga for you so that you never have to bother checking for updates again.")
        filemenu.AppendSeparator()
        menuExit=filemenu.Append(wx.ID_EXIT,"&Exit","Exit")
        menuBar=wx.MenuBar()
        menuBar.Append(filemenu,"&Actions")
        self.SetMenuBar(menuBar)
        #bind menu events
        self.Bind(wx.EVT_MENU, self.OnAdd, menuAdd)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
    def OnAddData(self,event):
        row=[str(self.AP.name.GetValue()),
        str(self.AP.url.GetValue()),
        str(self.AP.chIn.GetValue()),
        str(self.AP.btype.GetValue())]
        for r in row:
            if r == '':
                dlg = wx.MessageDialog(self,'Please fill all fields to add item to list','Warning!', wx.OK|wx.ICON_ERROR|wx.CENTRE|wx.STAY_ON_TOP)
                dlg.ShowModal()
                return
        if not row[2].isdigit():
            dlg = wx.MessageDialog(self,'Chapter number must be a interger','Warning!', wx.OK|wx.ICON_ERROR|wx.CENTRE|wx.STAY_ON_TOP)
            dlg.ShowModal()
            return
        fl=[]
        with open('aist.csv', newline='') as f:  
            reader = csv.reader(f,delimiter=',')
            for vali in reader:
                if(vali[0]==row[0]):
                    dlg = wx.MessageDialog(self,'Item with same name already exists.Please change Name','Warning!', wx.OK|wx.ICON_ERROR|wx.CENTRE|wx.STAY_ON_TOP)
                    dlg.ShowModal()
                    return
                fl.append(vali)
        fl.append(row)
        with open('aist.csv', 'w',newline='') as f:  
            writer = csv.writer(f,delimiter=',')
            for row in fl:
                writer.writerow(row)
        self.AP.clearForm()
        self.AP.Hide()
        self.LP.reload()
        self.LP.Show()
        self.Layout()
    def OnEditData(self,event):
        row=[str(self.EP.name.GetValue()),
        str(self.EP.url.GetValue()),
        str(self.EP.chIn.GetValue()),
        str(self.EP.btype.GetValue())]
        for r in row:
            if r == '':
                dlg = wx.MessageDialog(self,'Please fill all fields to add item to list','Warning!', wx.OK|wx.ICON_ERROR|wx.CENTRE|wx.STAY_ON_TOP)
                dlg.ShowModal()
                return
        if not row[2].isdigit():
            dlg = wx.MessageDialog(self,'Chapter number must be a interger','Warning!', wx.OK|wx.ICON_ERROR|wx.CENTRE|wx.STAY_ON_TOP)
            dlg.ShowModal()
            return
        for vali in self.EP.flo:
            if(vali[0]==row[0]):
                dlg = wx.MessageDialog(self,'Item with same name already exists.Please change Name','Warning!', wx.OK|wx.ICON_ERROR|wx.CENTRE|wx.STAY_ON_TOP)
                dlg.ShowModal()
                return
        self.EP.flo.append(row)
        with open('aist.csv', 'w',newline='') as f:  
            writer = csv.writer(f,delimiter=',')
            for row in self.EP.flo:
                writer.writerow(row)
        self.EP.fillForm('','','','')
        self.EP.Hide()
        self.LP.reload()
        self.LP.Show()
        self.Layout()
    def OnAdd(self,event):
        self.DP.Hide()
        self.EP.Hide()
        self.LP.Hide()
        self.AP.Show()
        self.Layout()
    def OnDetails(self,event):
        i=self.LP.llist.GetSelectedItemCount()
        if i==1:
            i=int(self.LP.llist.GetFirstSelected())
            fl=[]
            with open('aist.csv', newline='') as f:  
                reader = csv.reader(f,delimiter=',')
                ix=0
                for row in reader:
                    if ix==(i+1):
                        fl=list(row)
                        break
                    ix+=1
            self.DP.fillForm(fl[0],fl[2],fl[1],fl[3])
            self.AP.Hide()
            self.EP.Hide()
            self.LP.Hide()
            self.DP.Show()
            self.Layout()
        else:
            dlg = wx.MessageDialog(self, 'Please select exactly one item from the list','Warning!', wx.OK|wx.ICON_ERROR|wx.CENTRE|wx.STAY_ON_TOP)
            dlg.ShowModal()
    def OnEdit(self,event):
        i=self.LP.llist.GetSelectedItemCount()
        if i==1:
            i=int(self.LP.llist.GetFirstSelected())
            fl=[]
            self.EP.flo=[]
            with open('aist.csv', newline='') as f:  
                reader = csv.reader(f,delimiter=',')
                ix=0
                for row in reader:
                    if ix==(i+1):
                        ix+=1
                        fl=list(row)
                        continue
                    self.EP.flo.append(row)
                    ix+=1
            self.EP.fillForm(fl[0],fl[2],fl[1],fl[3])
            self.AP.Hide()
            self.DP.Hide()
            self.LP.Hide()
            self.EP.Show()
            self.Layout()
        else:
            dlg = wx.MessageDialog(self, 'Please select exactly one item from the list to edit','Warning!', wx.OK|wx.ICON_ERROR|wx.CENTRE|wx.STAY_ON_TOP)
            dlg.ShowModal()
    def OnGoBack(self,event):
        self.DP.Hide()
        self.EP.Hide()
        self.AP.Hide()
        self.LP.Show()
        self.Layout()
    def OnExit(self,event):
        self.Close(True)

app=wx.App(False)
frame=MainWindow(None,"WMC")
app.MainLoop()
