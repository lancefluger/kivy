from random import random
from kivy.graphics import Line, Color
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.app import App


class TouchTracer(Widget):
    def on_touch_down(self, touch):
        with self.canvas:
            touch.ud['color'] = Color(random(), 1, 1, mode='hsv')
            touch.ud['trace'] = Line()

        info_text = "Device: %s\nPos: %s\nID: %s" %(touch.device, touch.pos, touch.id)
        touch.ud['label'] = Label(text=info_text, pos=touch.pos)
        self.add_widget(touch.ud['label'])

    def on_touch_move(self, touch):
        touch.ud['trace'].points += touch.pos
        touch.ud['label'].pos = touch.pos

    def on_touch_up(self, touch):
        self.canvas.remove(touch.ud['trace'])
        self.remove_widget(touch.ud['label'])


class TouchTracerApp(App):
    def build(self):
        return TouchTracer()


if __name__ == "__main__":
    TouchTracerApp().run()

            

