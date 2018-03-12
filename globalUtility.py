import time
import datetime
import os
import json


RESET_HOUR = 999
mainDispOpen = False
#throw everything into appdata, why not
SETTINGS_FILE_PATH = os.getenv('APPDATA') + "\daystarter\settings.json"
SETTINGS_DIR_PATH = os.getenv('APPDATA') + "\\daystarter\\"
ICON_PATH = os.getenv('APPDATA') + "\\daystarter\\icons\\"

def getTime():
    now = datetime.datetime.now()
    return now

#initial setting of value, used for creating file
def initSettings():
    print "ininit"
    data = createEmptySettingsJson()
    
    try:
        os.makedirs(SETTINGS_DIR_PATH)
    except OSError as e:
        if e.errno == errno.EEXIST:
            pass
        else:
            print "problems creating directory", e
    
    try:
        with open(SETTINGS_FILE_PATH, 'w') as outfile:  
            json.dump(data, outfile)
    except IOError as e:
        print "Trouble opening file", e   

#load values from file (if exists)
def loadSettings():
    updateResetHour()
    #whatever other settings added in the future
   
#read from file to update global resetHour variable
def updateResetHour():
    settingsData = readFromFile()
    
    global RESET_HOUR
    if settingsData['resetHour'] == '':
         RESET_HOUR = 999
    else:
        RESET_HOUR = settingsData['resetHour']


def getResetHour():
    return RESET_HOUR
            
def readFromFile():
    
    try:
        with open(SETTINGS_FILE_PATH) as data_file:    
            data = json.load(data_file)
            
    except IOError as e:
        print 'Trouble opening file to read', e
        exit(1)
    else:
        return data
            
            
def writeToFile(data):
    try:
        with open(SETTINGS_FILE_PATH, 'w') as outfile:  
            json.dump(data, outfile)
            
    except IOError as e:
        print 'Trouble opening file to write', e
        exit(1)
    else:
        updateResetHour()
        
        
def createEmptySettingsJson():
    data = {}
    data['websites'] = []
    data['applications'] = []
    data['resetHour'] = ''
    
    return data
            