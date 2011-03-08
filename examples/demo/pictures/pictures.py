import glob
import random
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.scatter import Scatter
from kivy.animation import Animation
from kivy.properties import NumericProperty, StringProperty


class Picture(Scatter):
    filename = StringProperty('')
    x_accell = NumericProperty(0.0)
    y_accell = NumericProperty(0.0)

    def on_x_accell(self, *args):
        self.x += self.x_accell * .5

    def on_y_accell(self, *args):
        self.y += self.y_accell * .5

    def on_touch_up(self, touch):
        if super(Picture, self).on_touch_up(touch):
            self.x_accell = touch.dx
            self.y_accell = touch.dy
            Animation(x_accell=0., y_accell=0., t='out_quad', d=.5).start(self)
            return True


class PicturesApp(App):

    def build(self):
        for filename in glob.glob('images/*'):
            self.add_picture(filename)

    def add_picture(self, filename):
        scatter = Picture(filename=filename)
        scatter.center = Window.center
        scatter.rotation = random.randint(-30, 30)
        self.root.add_widget(scatter)

if __name__ in ('__main__', '__android__'):
    PicturesApp().run()

