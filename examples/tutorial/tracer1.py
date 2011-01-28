from kivy.graphics import Line
from kivy.uix.widget import Widget
from kivy.app import App


class TouchTracer(Widget):
    def on_touch_down(self, touch):
        touch.ud['trace'] = Line()
        self.canvas.add(touch.ud['trace'])

    def on_touch_move(self, touch):
        touch.ud['trace'].points += touch.pos

    def on_touch_up(self, touch):
        self.canvas.remove(touch.ud['trace'])


class TouchTracerApp(App):
    def build(self):
        return TouchTracer()

if __name__ == "__main__":
    TouchTracerApp().run()

            
