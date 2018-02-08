# This module will the UI for the application, which will
# allow user to setup the configuration required and
# start the service

from kivy.app import App
from os.path import join
from os import getcwd
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty
import re
from collections import OrderedDict, Counter
from sys import exit
from kivy.clock import Clock
from kivy.config import Config

Builder.load_file('parentex.kv')

Config.set('graphics', 'width', '550')
Config.set('graphics', 'height', '800')
Config.write()


class PinEntry(TextInput):
    name = StringProperty('')  # define the name of the TextInput

    pat = re.compile('[^0-9]')
    pinIDs = OrderedDict({1: 'PIN1', 2: 'PIN2', 3: 'PIN3', 4: 'PIN4'})

    def __init__(self, **kwargs):
        super(PinEntry, self).__init__(**kwargs)

    def getIndx(self, myId):
        idx = [(k, v) for k, v in self.pinIDs.items() if v == myId]
        if len(idx) > 0:
            return idx[0][0]
        else:
            return 0

    def getNextPIN(self, myId):
        indx = self.getIndx(myId)
        # next indx
        indx += 1
        if indx > 0 and indx > 4:
            return 'PIN1'
        else:
            return 'PIN' + str(indx)

    def readyToTryLogin(self):
        # check if every box has some number
        for pinID in self.pinIDs.values():
            if self.parent.parent.parent.ids[pinID].text == '':
                return False

        return True

    def getPIN(self):
        # concatenate the pin digits and return
        pin = ""
        for pinID in self.pinIDs.values():
            pin += self.parent.parent.parent.ids[pinID].text

        return pin

    def loginVerified(self):
        pinEntered = self.getPIN()

        with open(join(getcwd(), "trouble.dat"), "r") as f:
            pin = f.readline()
            # check if pin matches
            pin = pin.replace('\n', '')
            if pin == pinEntered:
                return True
            else:
                return False

    def resetPinNow(self, dt):
        for pinID in self.pinIDs.values():
            self.parent.parent.parent.ids[pinID].text = ''

    def resetPinEntry(self):
        # schedule the call so, we dont' have recursion
        Clock.schedule_once(self.resetPinNow, 1)

    def insert_text(self, substring, from_undo=False):
        #  let only numeric and only one number
        try:
            pat = self.pat
            # reset the label with no messages
            self.parent.parent.parent.ids["loginLbl"].text = ""

            s = re.sub(pat, '', substring)
            # only one last digit is allowed
            if s != '':
                s = s[len(s) - 1]
                self.text = s

            # verify if all boxes got some number
            # if so, try to login
            if self.readyToTryLogin():
                # display text
                self.parent.parent.parent.ids["loginLbl"].text = \
                    "Trying to login..."

                # try login
                if self.loginVerified():
                    # move to next screen
                    appScreens.current = "mainPg"
                else:
                    # reset the text boxes
                    # show the message and set focus to first box
                    self.parent.parent.parent.ids["loginLbl"].text = \
                        "Wrong PIN, try again..."
                    self.resetPinEntry()
                    self.parent.parent.parent.ids["PIN1"].focus = True
            else:
                # move the focus to the next text box
                self.parent.parent.parent.ids[self.getNextPIN(
                    self.name)].focus = True

            return True

        except(Exception) as e:
            # set the label with comments
            self.parent.parent.parent.ids["loginLbl"].text = "Exception : " \
                + str(e)

            return True


class ScheduleEntry(TextInput):
    # Custom Text Input box

    pat = re.compile('[^0-9(),]')

    def __init__(self, **kwargs):
        super(ScheduleEntry, self).__init__(**kwargs)

    def insert_text(self, substring, from_undo=False):
        #  let only numeric and only one number
        pat = self.pat

        s = re.sub(pat, '', substring)

        return super(ScheduleEntry, self).insert_text(s, from_undo=from_undo)


class LoginScreen(Screen):
    pass


class MainScreen(Screen):
    pass


class ParentExApp(App):

    def build(self):
        return appScreens

    def on_start(self, **kwargs):
        print("App started..")

    def saveDataToFile(self, schText):
        # save the file to local file
        with open(join(getcwd(), "schedule.dat"), 'w') as f:
            f.write(schText)

    def minutes(self, tmStr):
        # convert the time into minutes
        # format of input param can be hr:min or hr
        totMinutes = 0
        hrMin = str(tmStr).split(":")

        totMinutes = int(hrMin[0]) * 60

        if len(hrMin) > 1:
            totMinutes += int(hrMin[1])

        return totMinutes

    def convertToMinutes(self, schList):
        # items in the list is hr:min, hr:min or hr, hr

        minList = [(self.minutes(fM), self.minutes(tM)) for fM, tM in schList]

        return minList

    def validate_input(self, txt, statusLbl):
        # returns error if invalid entry else save the value in a text file
        retValue = "Input values validated successfully and saved..."
        err = False

        try:
            # expecting a list of tuples
            # when there is one schedule, we have to handle it differently
            # to satisfy the eval default implementation limitation
            schList = []
            initList = list(eval(txt))

            c = Counter(txt)
            # if there is one comma, then its one schedule
            if c[','] == 1:  # count
                schList.append(tuple(initList))
            else:
                schList = initList[:]  # copy the values

            # convert to minutes before saving the file
            schList = self.convertToMinutes(schList)

            # expecting the from hr to be less than to hour
            if True in [f >= t or (f > 1438 or t > 1440) or (f < 0 or t < 0)
                        for f, t in schList]:
                retValue = "Values not valid, 'From' hour cannot be greater \
                than 'To' hour or Hour cannot be less than One or greater \
                than 24"

                retValue = retValue.replace('  ', '')
                err = True
            else:
                print("Saving data.. " + txt)

                self.saveDataToFile(str(schList))

        except(Exception) as e:
            retValue = "Exception : " + str(e)
            err = True

        statusLbl.text = retValue

        if err:
            statusLbl.color = (.7, .01, .2, 1)
        else:
            statusLbl.color = (0, 1, .7, 1)

    def cancel_pressed(self):
        # exit the app
        exit(0)


appScreens = ScreenManager()
appScreens.add_widget(LoginScreen(name="login"))
appScreens.add_widget(MainScreen(name="mainPg"))


if __name__ == "__main__":

    ParentExApp().run()
