#!/usr/bin/env python
import psutil
import tkinter as tk
import tkinter.scrolledtext as tkscrtxt


class Process():
    
    
    def getListOfAllRunningProcesses(self):
        processes=list()
        for i, proc in enumerate(psutil.process_iter()):
            try:
                processInfo=proc.as_dict(attrs=['pid', 'name'])
                processes.append(processInfo)
                #print(str(i)+") ", end=" ")
                #print(processInfo)
            except psutil.NoSuchProcess:
                pass
        return processes
        
        
    def terminateProcess(self,pid):
        try:
            proc= psutil.Process(pid)
            proc.terminate() 
        except psutil.NoSuchProcess:
            pass
        return processes   
        
        
        
        
class UI():
        
        def __init__(self,title="OS unwanted processes"):
            self.window = tk.Tk()
            self.window.title(title)
            self.window.resizable(20, 20)
            self.processes= Process().getListOfAllRunningProcesses()
            self.setupUi(self.window)
            self.window.mainloop()
        
        def setupUi(self,win):
            warningLabel = tk.Label(master=win, text="There are other instances of these tools on, Do you wanna kill them all?") 
            warningLabel.grid(column=0, row=0)
            warningLabel.configure(foreground='red')

            #processesScrText = tkscrtxt.ScrolledText(win, width=30, height=3,wrap=tk.WORD) 
            #processesScrText.grid(column=0, row=2)
            #processesScrText.grid(column=0, columnspan=3)
            procFrame=tk.Frame(master=win)
            procFrame.grid(column=0, row=1)
            self.listbox = tk.Listbox(master=procFrame,selectmode=tk.EXTENDED,width=50)
            self.listbox.grid(column=0, row=1)
            self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
            self.listbox.insert(tk.END, "PROCESSES")
            for processInfo in self.processes:
                self.listbox.insert(tk.END, processInfo['name'])
            
            self.killButton=tk.Button(master=win, text="kill all", command=self.killProcessesCmd)
            self.killButton.grid(column=0, row=3)
            
        def killProcessesCmd(self):
            procNames=self.listbox.get(0, tk.END)
            for processInfo in self.processes:
                self.killButton.configure(text='Hello ')
                if(any(procN ==processInfo['name'] for procN in procNames)):
                    Process().terminateProcess(processInfo['pid'])
        
        
        
if __name__ == "__main__":
    process= Process()
    ui= UI()
    # print(process.getListOfAllRunningProcesses())
    # for processInfo in process.getListOfAllRunningProcesses():
        # if(processInfo['name']=='qtcreator.exe'):
            # process.terminateProcess(processInfo['pid'])