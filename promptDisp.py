#Controls the display of the prompt and saving of variables
import globalUtility as GU
from kivy.clock import Clock
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import kivy.core.window as window
from kivy.base import EventLoop
from kivy.config import Config

stopEvent = ""

class MainDisplay(BoxLayout):

    def __init__(self, **kwargs):
        super(MainDisplay, self).__init__(**kwargs)
        self.checkForEventSet = Clock.schedule_interval(self.stopOnEventSet, 1)
        self.orientation = 'vertical'
        
        window.Window.size = (600, 400)
        self.popupOpen = False
        
        #website input
        self.browserSettingsLayout = BoxLayout(padding=5)
        self.browserSettingsLayout.orientation = 'horizontal'
        self.browserSettingsLayout.add_widget(Label(text='Browser Tabs', size_hint=(.33,1.0)))
        self.browserTabsToOpen = TextInput(multiline=True)
        self.browserSettingsLayout.add_widget(self.browserTabsToOpen)
        self.add_widget(self.browserSettingsLayout)
        
        #apps input
        self.applicationsSettingsLayout = BoxLayout(padding=5)
        self.applicationsSettingsLayout.orientation = 'horizontal'
        self.applicationsSettingsLayout.add_widget(Label(text='Apps To Launch', size_hint=(.33,1.0)))
        self.appsToOpen = TextInput(multiline=True)
        self.applicationsSettingsLayout.add_widget(self.appsToOpen)
        self.add_widget(self.applicationsSettingsLayout)
        
        #splitter
        self.splitLayout = BoxLayout(padding=0)
        self.splitLayout.orientation = 'horizontal'
        self.splitLayout.add_widget(Label(text='-----Settings-----', size_hint=(1.0,1.0)))
        self.add_widget(self.splitLayout)
        
        #reset hour input
        self.miscSettingLayout = BoxLayout(padding=5)
        self.miscSettingLayout.orientation = 'horizontal'
        self.miscSettingLayout.add_widget(Label(text='Reset Time\n(Hour 0-23)', size_hint=(.33,1.0)))
        self.resetHour = TextInput(input_filter='int',  size_hint=(.33,1))
        self.miscSettingLayout.add_widget(self.resetHour)
        self.miscSettingLayout.add_widget(Label(text='',  size_hint=(.33,1.0)))
        self.add_widget(self.miscSettingLayout)
        
        #apply button
        self.buttonLayout = BoxLayout(padding=5)
        self.buttonLayout.orientation = 'horizontal'
        #dummy
        self.buttonLayout.add_widget(Label(text=''))
        self.applyButton = Button(text="Apply")
        self.applyButton.bind(on_press=self.updateSettingsFile)
        self.buttonLayout.add_widget(self.applyButton)
        #dummy
        self.buttonLayout.add_widget(Label(text=''))
        self.add_widget(self.buttonLayout)
                  
        
        #fill in existing input
        self.setPromptValues()
      
    def updateSettingsFile(self, btn):
        """write to json file"""
        #replicate empty json structure
        settingsData = GU.createEmptySettingsJson()
        
        #set sites to open
        for line in self.browserTabsToOpen.text.split('\n'):
        #filter out accidental new lines (especially at ends)
            if line == "":
                pass
            else:
                settingsData['websites'].append({
                    'URL' : line
                })
                
        #set programs to open
        for line in self.appsToOpen.text.split('\n'):
            if line == "":
                pass
            else:
                settingsData['applications'].append({
                    'path' : line
                })
                
        #set settings        
        settingsData['resetHour'] = self.resetHour.text
            
        #attempt to write
        GU.writeToFile(settingsData)
        
        #change visual feedback to indicate that a change was made
        self.changeApplyButtonColorSuccess()
        Clock.schedule_once(self.resetApplyButtonColor, 1.5)
        
                
    def setPromptValues(self):
        """fill out prompt if values have already been saved"""
        
        settingsData = GU.readFromFile()
            #get sites
        stringSites = ""
        for site in settingsData['websites']:
            stringSites += site['URL'] + "\n"
           
        #get apps
        stringApps = ""
        for app in settingsData['applications']:
            stringApps += app['path'] + "\n"
           
        #remove last newline
        stringApps = stringApps[:-1]
        stringSites = stringSites[:-1]
           
        #set prompt values
        self.browserTabsToOpen.text = stringSites
        self.appsToOpen.text = stringApps
        if settingsData['resetHour'] != '':
            self.resetHour.text = str(settingsData['resetHour'])
            
    def stopOnEventSet(self, dt):
        global stopEvent
        if stopEvent.isSet():
            app = App.get_running_app()
            app.stop()
            window.Window.close()
        else:
            pass
            
        
    def resetApplyButtonColor(self, dt):
        '''reset button'''
        self.applyButton.disabled = False
        self.applyButton.background_color = (1,1,1,1)
        self.applyButton.text = "Apply"
        
        
    def changeApplyButtonColorSuccess(self):
        '''show that changes were made by changing button color and text'''
        self.applyButton.background_disabled_normal = ''
        self.applyButton.disabled = True
        self.applyButton.background_color = (.2,.8,.2,.3)
        self.applyButton.text = "Changes Saved"
        
    
class MyApp(App):

    def build(self):
        self.title = 'Daycreator'
        iconString = GU.ICON_PATH + 'main_.ico'
        self.icon = iconString
        
        return MainDisplay()
        
    #cleanup
    def on_stop(self):
        self.closeScheduledEvents()  
        GU.mainDispOpen = False 

    #kivy liked to keep events scheduled even after app closed
    #this closes all events made by tthe previous window
    def closeScheduledEvents(self):
        for event in Clock.get_events():
            Clock.unschedule(event)
                
                
def showPrompt(stopEventHandle):
    '''builds app GUI'''
    global stopEvent
    stopEvent = stopEventHandle
    
    if GU.mainDispOpen == False:
        GU.mainDispOpen = True
        resetKivyCache()
        MyApp().run()
        
    else:
        pass
#kivy has problems opening up twice in the same run, workaround
def resetKivyCache():
    
    if not EventLoop.event_listeners:
        from kivy.cache import Cache
        window.Window = window.core_select_lib('window', window.window_impl, True)
        for cat in Cache._categories:
            Cache._objects[cat] = {}
    

                
    