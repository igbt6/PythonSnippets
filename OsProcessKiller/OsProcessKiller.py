#!/usr/bin/env python
import psutil
import sys
import os
import logging
import tkinter as tk
import tkinter.scrolledtext as tkscrtxt
import tkinter.scrolledtext
from tkinter import ttk
from tkinter import messagebox as msgBox
import copy

#BUILD OPTIONS:
#pyinstaller --noconsole --onefile OsProcessKiller.py
logger = logging.getLogger('OsProcessKileer')
logger.setLevel(logging.NOTSET)

class Process:
    
    def __init__(self):
        self.__unwantedProcesses= self.readUnwantedProcesses("UnwantedProcesses.txt")
        logger.debug("self.__unwantedProcesses"+''.join(self.__unwantedProcesses))
        
    def getListOfAllRunningProcesses(self):
        processes=list()
        for i, proc in enumerate(psutil.process_iter()):
            try:
                processInfo=proc.as_dict(attrs=['pid', 'name','username'])
                processes.append(processInfo)
                logger.debug(processInfo)
            except psutil.NoSuchProcess:
                pass
        return processes
                
    def terminateProcess(self,pid):
        try:
            proc= psutil.Process(pid)
            proc.terminate() 
        except psutil.NoSuchProcess:
            pass 
      
    def getUnwantedProcesses(self):
        return self.__unwantedProcesses
    
    def readUnwantedProcesses(self,unwantedProcessesFilePath):
        if(not os.path.exists(unwantedProcessesFilePath)):
            raise IOError("unwantedProcessesFilePath does not exist")
        unwantedProcessesList=[]
        try:
            with open(unwantedProcessesFilePath,'r+') as f:
                openContentFlag =0
                for nrOfLine, line in enumerate(f):
                    if(line.find("//UNWANTED_PROCESSES//")is not -1):
                        openContentFlag =1
                    elif(line.find("//UNWANTED_PROCESSES_END//")is not -1):
                        openContentFlag =2
                        break
                    elif openContentFlag ==1:
                        unwantedProcessesList.append(line.rstrip('\n').rstrip('\r').rstrip(" "))
        except IOError as e:
            logger.debug('[ERROR] Unable to open file:%s, ERROR: %s'%unwantedProcessesFilePath % e.strerror)
            sys.exit(1)
        except ValueError as e:
            logger.debug('[ERROR] %s' %e)
            sys.exit(1)
        return unwantedProcessesList
             
        
AppName="OS unwanted processes' killer"       

def createMessageBox( msg, title=AppName, type='WARNING'):
    '''
        possible types: WARNING, INFO,ERROR
    '''
    if type=='WARNING':
        msgBox.showwarning(title, msg)   
    elif type=='INFO':
        msgBox.showinfo(title, msg)
    elif type=='ERROR':
        msgBox.showerror(title, msg)
    else: 
        return

class App():
                
        def __init__(self,title=AppName):
            self.window = tk.Tk()
            self.window.title(title)
            #self.window.resizable(20, 20)
            width=470
            height=350
            ws = self.window.winfo_screenwidth() # width of the screen
            hs = self.window.winfo_screenheight() # height of the screen
            x = (ws/2) - (width/2)
            y = (hs/2) - (height/2)
            self.window.geometry('%dx%d+%d+%d' % (width, height, x, y))            
            self.process= Process() #process object
            self.setupUi(self.window)
            self.window.mainloop()
               
        def setupUi(self,win):
            warningLabel = tk.Label(master=win, text="There are other instances of these apps running on, Do you wanna kill them all?") 
            warningLabel.grid(in_=win, row=0, column=0, sticky=tk.NW)
            warningLabel.configure(foreground='red')
            
            processLabel= tk.Label(master=win, text="PROCESSES:")
            processLabel.grid(in_=win, row=1, column=0, sticky=tk.NW)
           
            self.createProcessView(win)
            self.createChooserView(win)
            
            self.killButton=tk.Button(master=win, text="Kill all checked processes", command=self.killProcessesCb,height=3,width = 30)
            self.killButton.grid(in_=win,row=3, column=0,sticky=tk.N)
         
        def createProcessView(self, parent):
            frame= ttk.Frame(master=parent,width=150)
            #frame.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.Y) 
            frame.grid(in_=parent, row=2, column=0, sticky=tk.NSEW)            
            # create the tree and scrollbars
            self.processTreeDataColumns = ('NAME', 'PID', 'USER')       
            self.processTree = ttk.Treeview(columns=self.processTreeDataColumns,show = 'headings',selectmode=tk.EXTENDED)
            for c in self.processTreeDataColumns:
                    self.processTree.heading(c, text=c)
            for col in self.processTreeDataColumns:
                self.processTree.column(col,minwidth=0,width=150, stretch=tk.YES)
            processTreeYsb = ttk.Scrollbar(orient=tk.VERTICAL, command= self.processTree.yview)
            processTreeXsb = ttk.Scrollbar(orient=tk.HORIZONTAL, command= self.processTree.xview)
            self.processTree['yscroll'] = processTreeYsb.set
            self.processTree['xscroll'] = processTreeXsb.set
            
            #adds process tree and scrollbars to frame
            self.processTree.grid(in_=frame, row=0, column=0, sticky=tk.NSEW)
            processTreeYsb.grid(in_=frame, row=0, column=1, sticky=tk.NS)
            processTreeXsb.grid(in_=frame, row=1, column=0, sticky=tk.EW)
            
            frame.rowconfigure(0, weight=1)
            frame.columnconfigure(0, weight=1)
                      
            #fetch data into Tree View
            self.updateProcessDataInTreeView()
        
        def createChooserView(self,parent):
            frame= ttk.Frame(master=parent)
            frame.grid(in_=parent, row=3, column=0, sticky=tk.NW)            
            # create check button
            self.checkAllButtonVar= tk.IntVar()
            self.checkAllButtonVar.set(0)
            checkAllButton = tk.Checkbutton(master=frame, text = "Check All", variable = self.checkAllButtonVar, \
                 onvalue = 1, offvalue = 0, height=5, \
                 width = 20, command=self.checkAllItemsCb )
            #checkAllButton.var=self.checkAllButtonVar
            checkAllButton.pack()
            frame.rowconfigure(0, weight=1)
            frame.columnconfigure(0, weight=1)
        

        
        #methods concerning data handling
        def fetchProcessData(self,data):
            if len(data)==0 or data== None:
                raise ValueError("process data cannot be empty !")
            if not(len(data[0])==3):
                raise ValueError("process data item must contain NAME, PID and USER attrs! ")
            #self.processData = data
            #self.processData = copy.copy(data) 
            #self.processData = copy.deepcopy(data)              
            for i,item in enumerate(data):
                self.processTree.insert(parent='',iid=i+1,index=tk.END, values=item)
        
        def convertAllProcessesToTreeViewFormat(self, processesData):
            '''
                processesData list of dicts of format: dict{'name':___, 'username':___, 'pid':___ }
            '''
            if len(processesData)==0 or processesData==None:
                raise ValueError("process data cannot be empty !")
            if not(len(processesData[0])==3):
                raise ValueError("process data item must contain NAME, PID and USER attrs! ")
            return[(proc['name'],proc['pid'],proc['username']) for proc in processesData]
        
        def createListOfUnwantedProcesses(self, unwantedProcessList):
            if len(unwantedProcessList)==0 or unwantedProcessList==None:
                raise ValueError("unwantedProcessList cannot be empty !")
            listOfUnwantedProcesses=[(processInfo) for processInfo in self.process.getListOfAllRunningProcesses() for item in unwantedProcessList if processInfo['name']==item]
            return listOfUnwantedProcesses
          

        def updateProcessDataInTreeView(self):
            try:
                processData = self.convertAllProcessesToTreeViewFormat(self.createListOfUnwantedProcesses(self.process.getUnwantedProcesses()))
                self.clearAllItemsFroTreeView()
                self.fetchProcessData(processData)
            except Exception as e:
                logger.debug("No more process to be killed, close the app!" +str(e))
                #createMessageBox( msg="There is no more unwanted processes to be killed, close the app", type='INFO')               
                sys.exit(1) #TODO maybe add messagebox that no more processes exist?
                
        def clearAllItemsFroTreeView(self):
            for item in self.processTree.get_children():
                self.processTree.delete(item)
                 
        #callbacks
        def killProcessesCb(self):
            procNames=[self.processTree.item(child)['values'][0] for child in self.processTree.selection()]
            logger.debug(procNames)
            if(len(procNames)==0):
                return         
            for processInfo in self.process.getListOfAllRunningProcesses():
                #self.killButton.configure(text='Killing...')
                if(any(procN ==processInfo['name'] for procN in procNames)):
                    self.process.terminateProcess(processInfo['pid'])
                    #map(self.processTree.delete, self.processTree.get_children())
                    self.updateProcessDataInTreeView()
            #self.killButton.configure(text='Done!')
        
        def checkAllItemsCb(self):
            if self.checkAllButtonVar.get() ==1:
                self.processTree.selection_set(self.processTree.get_children(''))
            else:
                self.processTree.selection_remove(self.processTree.get_children(''))
                
             
        
if __name__ == "__main__":
    try:
        app= App()
    except Exception as e:
        logger.debug(str(e))
        createMessageBox( msg=str(e), type='ERROR')  
        sys.exit(1)
        
    