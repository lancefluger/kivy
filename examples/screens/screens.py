__all__ = ('FboFloatLayout', )


from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, Canvas, ClearBuffers, ClearColor
from kivy.graphics.fbo import Fbo
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty, NumericProperty, StringProperty


from screen_shaders import *


class Screen(FloatLayout):
    alpha = NumericProperty(1.0)
    fbo = ObjectProperty(None, allownone=True)
    texture = ObjectProperty(None, allownone=True)
    vs_shader = StringProperty(vs_slide_right)
    fs_shader = StringProperty(fs_opacity)

    def __init__(self, **kwargs):
        self.canvas = Canvas()
        with self.canvas:
            self.fbo = Fbo(size=self.size)
            self.fbo_color = Color(1, 1, 1, 1)
            self.fbo_rect = Rectangle()

        with self.fbo:
            ClearColor(0,0,0,0)
            ClearBuffers()
        # wait that all the instructions are in the canvas to set texture
        self.texture = self.fbo.texture
        super(Screen, self).__init__(**kwargs)

        self.fbo.shader.fs = self.fs_shader
        self.fbo.shader.vs = self.vs_shader
        self.fbo['size'] = map(float, self.size)
        self.fbo['alpha'] = self.alpha

    def add_widget(self, *largs):
        # trick to attach graphics instructino to fbo instead of canvas
        canvas = self.canvas
        self.canvas = self.fbo
        ret = super(Screen, self).add_widget(*largs)
        self.canvas = canvas
        return ret

    def remove_widget(self, *largs):
        canvas = self.canvas
        self.canvas = self.fbo
        super(Screen, self).remove_widget(*largs)
        self.canvas = canvas

    def to_local(self, x, y, relative=True):
        return (x - self.x, y - self.y)

    def on_texture(self, instance, value):
        self.fbo_rect.texture = value

    def on_pos(self, instance, value):
        self.fbo_rect.pos = value

    def on_size(self, instance, value):
        self.fbo.size = value
        self.fbo['size'] = map(float, value)
        self.texture = self.fbo.texture
        self.fbo_rect.size = value

    def on_fs_shader(self, instance, value):
        self.fbo.shader.fs = value

    def on_vs_shader(self, instance, value):
        self.fbo.shader.vs = value

    def on_alpha(self, instance, value):
        print self, value
        self.fbo['alpha'] = float(value)
        self.fbo.ask_update()

    def on_touch_down(self, touch):
        touch.push()
        touch.apply_transform_2d(self.to_local)
        if super(Screen, self).on_touch_down(touch):
            touch.pop()
            return True
        touch.pop()

    def on_touch_move(self, touch):
        touch.push()
        touch.apply_transform_2d(self.to_local)
        if super(Screen, self).on_touch_move(touch):
            touch.pop()
            return True
        touch.pop()

    def on_touch_up(self, touch):
        touch.push()
        touch.apply_transform_2d(self.to_local)
        if super(Screen, self).on_touch_up(touch):
            touch.pop()
            return True
        touch.pop()



from kivy.factory import Factory as F
F.register('Screen', Screen)



from kivy.app import App
from kivy.animation import Animation

class ScreenApp(App):
    def build(self):
        pass

if __name__ == "__main__":
    ScreenApp().run()
