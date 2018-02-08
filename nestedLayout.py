from kivy.app import App
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout


class HBoxWidget(Widget):
    def __init__(self, **kwargs):
        super(HBoxWidget, self).__init__(**kwargs)


class VBoxWidget(Widget):
    def __init__(self, **kwargs):
        super(VBoxWidget, self).__init__(**kwargs)


class ContainerBox(BoxLayout):
    def __init__(self, **kwargs):
        super(ContainerBox, self).__init__(**kwargs)


class TestApp(App):
    def build(self):
        return ContainerBox()


if __name__ == '__main__':
    TestApp().run()
