from random import random

from kivy.graphics import Canvas, Color, Line, Ellipse
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.app import App


class TracerGraphic(Canvas):

    def __init__(self, **kwargs):
        super(TracerGraphic, self).__init__(**kwargs)
        with self:
            self.init_canvas()

    def init_canvas(self):
        self.hue = random()
        self.t_color = Color(self.hue, 1, 1, 1, mode='hsv')
        self.trace = Line()
        self.r_color = Color(self.hue, 1, 1, 0.2, mode='hsv')
        self.ruler_v = Line()
        self.ruler_h = Line()
        self.circle = Ellipse(pos=(-30, -30), size=(30, 30))

    def add_point(self, p):
        x, y = p
        self.trace.points += p
        self.circle.pos = x - 15, y - 15
        self.ruler_v.points = [x, 0, x, 3000]
        self.ruler_h.points = [0, y, 3000, y]


class TouchTracer(Widget):

    def build_info_label(self, touch):
        info_text = "Device: %s\nPos: %s\nID: %s" % (
                touch.device,
                touch.pos,
                touch.id)
        info_label = Label(text=info_text, pos=touch.pos)
        return info_label

    def on_touch_down(self, touch):
        touch.ud['label'] = self.build_info_label
        self.add_widget(touch.ud['label'])
        with self.canvas:
            touch.ud['trace'] = TracerGraphic()

    def on_touch_move(self, touch):
        touch.ud['trace'].add_point(touch.pos)
        touch.ud['label'].pos = touch.pos

    def on_touch_up(self, touch):
        self.canvas.remove(touch.ud['trace'])
        self.remove_widget(touch.ud['label'])


class TouchTracerApp(App):

    def build(self):
        return TouchTracer()


if __name__ == "__main__":
    TouchTracerApp().run()

