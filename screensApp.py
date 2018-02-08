from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from os.path import join
from os import getcwd

# Create both screens. Please note the root.manager.current: this is how
# you can control the ScreenManager from kv. Each screen has by default a
# property manager that gives you the instance of the ScreenManager used.
Builder.load_string("""
<LoginScreen>

    GridLayout:
        cols: 5
        rows: 2
        
        canvas.before:
            Rectangle:
                pos: self.pos
                size: self.size
                source: 'login.jpg'            

        Label:
            text: "PIN: "
        TextInput:
            font_size: 30
            text: "0"
        TextInput:
            font_size: 30
            text: "0"
        TextInput:
            font_size: 30
            text: "0"
        TextInput:
            font_size: 30
            text: "0"
        Label:
            text: ""
        Label:
            text: ""
        Label:
            text: ""
        Button:
            text: "Login"
            on_press:
                root.manager.current = "settings"
        Label:
            text: ""


<Box1>
    BoxLayout:
        orientation: "horizontal"
        pos: root.pos
        size: root.size
        spacing: 10
        padding: 30

        canvas:
            Color:
                rgba: 0, 1, 0, 1
            Line: 
                rounded_rectangle: self.pos[0] + 5, self.pos[1] + 5, self.size[0] - (5*2), self.size[1] - (5*2), 10
        Label:
            text: "Time range:"
            font_size: 28
            color: 1, 1, 1, 1
            size_hint: .2, .3
        TextInput:
            text: "(9,10), (5, 7)"
            multiline: False
            font_size: 28
            color: 1, 1, 1, 1
            size_hint: .5, .3
            on_text_validate: 
                app.AppContainer.Box3.msg.text=app.validate_input(self.text)
            focus: True

<Box2>
    BoxLayout:
        orientation: "horizontal"
        pos: root.pos
        size: root.size
        spacing: 10
        padding: 10

        canvas:
            Color:
                rgba: 0, 1, 0, 1

            Line: 
                rounded_rectangle: self.pos[0] + 5, self.pos[1] + 5, self.size[0] - (5*2), self.size[1] - (5*2), 10

        Button:
            text: "Save"
            size_hint: .3, .3
        Button:
            text: "Cancel"
            size_hint: .3, .3
        Button:
            text: "Start Service"
            size_hint: .4, .3
            
<Box3>
    BoxLayout:
        orientation: "vertical"
        pos: root.pos
        size: root.size
        spacing: 10
        padding: 10

        canvas:
            Color:
                rgba: 0, 1, 0, 1

            Line: 
                rounded_rectangle: self.pos[0] + 5, self.pos[1] + 5, self.size[0] - (5*2), self.size[1] - (5*2), 10

        Label:
            id: msg
            text: "Status Message"


<SettingsScreen>
    BoxLayout:
        orientation: "vertical"
        canvas.before:
            Rectangle:
                pos: self.pos
                size: self.size
                source: 'download.jpg'            
        Box1:
        Box2:
        Box3:
""")

# Declare both screens


class Box1(Widget):
    def __init__(self, **kwargs):
        super(Box1, self).__init__(**kwargs)

    def saveDataToFile(self, schText):
        # save the file to local file
        with open(join(getcwd(), "schedule.dat"), 'w') as f:
            f.write(schText)

    def validate_input(self, txt):
        # returns error if invalid entry else save the value in a text file
        retValue = "Input values validated successfully and saved..."

        try:
            # expecting a list of tuples
            schList = eval(txt)

            # expecting the from hr to be less than to hour
            if False in [f >= t for f, t in schList]:
                retValue = "Values not valid, 'From' hour cannot be greater \
                than 'To' hour"

            self.saveDataToFile(txt)

        except(Exception) as e:
            retValue = "Exception : " + str(e)

        return retValue


class Box2(Widget):
    def __init__(self, **kwargs):
        super(Box2, self).__init__(**kwargs)


class Box3(Widget):
    def __init__(self, **kwargs):
        super(Box3, self).__init__(**kwargs)


class LoginScreen(Screen):
    pass


class SettingsScreen(Screen):
    pass


# Create the screen manager
sm = ScreenManager()
sm.add_widget(LoginScreen(name='login'))
sm.add_widget(SettingsScreen(name='settings'))


class TestApp(App):

    def build(self):
        return sm


if __name__ == '__main__':
    TestApp().run()
