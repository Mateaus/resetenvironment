# Reset Project
# Joe Finley
# 

import threading
import promptDisp as prompt
import globalUtility as GU
import os
import systray
from subprocess import Popen
import time
import webbrowser as wb



class ThreadedReset(threading.Thread):
    def __init__(self, stopEvent):
        super(ThreadedReset,self).__init__()
        self.stopEvent = stopEvent
        
    def run(self):
        
        while 1:
            self.waitUntilResetHourOrStopEvent()
            if self.stopEvent.isSet():
                return
            else:
                settingsData = GU.readFromFile()
                self.resetEnvironment(settingsData)
         
    #maybe add functionality here to set specific times such as 5:30       
    def waitUntilResetHourOrStopEvent(self):
        """returns when event is set or time is reached"""
        while GU.getTime().hour != int(GU.getResetHour() and GU.getTime().second == 0):
            time.sleep(1)
            if self.stopEvent.isSet():
                return 
        

    def resetEnvironment(self, dataFile):
        """closes browser, opens new browser with tabs set in settings, opens apps"""
        closeTabs()
        time.sleep(.3)
        openTabs(dataFile)
        time.sleep(.8)
        openApps(dataFile)
        
        
def closeTabs():
    """ closes old tabs (chrome) """
    try:
        Popen('taskkill /T /F /IM chrome.exe')
    except Exception as e:
        print e

def openTabs(data):
    """ opens new tab in default browser """
    #workaround. if http://www. does not exist, IE will open rather than default browser
    #check if www. exists, append http://www. to listings which do not have it
    for site in data['websites']:
        #test for none
        if site['URL']:
            if site['URL'].startswith("http://www."):
                wb.open_new_tab(site['URL'])
            else:
                wb.open_new_tab("http://www." + site['URL'])
            
            
def openApps(data):
    """ opens programs specified by exe files in the applications index"""
    for executable in data['applications']:
        #test for none
        if executable['path']:
            try:
                Popen(executable['path'])
            except OSError as e:
                print "Trouble opening executable. Please provide a correct executable (.exe) file", e
                
if __name__ == '__main__':
    
    stopEvent = threading.Event()
    
    #create file if file doesnt exist, init with default values. else load global variables
    if(os.path.isfile(GU.SETTINGS_FILE_PATH) == False ):
        print "init"
        GU.initSettings()
    else:
        GU.loadSettings()
        
    #delegate reset logic to seperate thread
    resetThread = ThreadedReset(stopEvent)
    resetThread.start()
    

    sysTrayThread = threading.Thread(target=systray.initSystray, args=(stopEvent,))
    sysTrayThread.start()
    
    
    #open initial prompt, create systray functionality
    prompt.showPrompt(stopEvent)
    
    #join thread to main
    sysTrayThread.join()
    resetThread.join()
    
   
    
    
    

   

    
    
    
         
    
    