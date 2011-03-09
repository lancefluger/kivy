'''
ScrollView widget
'''

__all__ = ('ScrollView', )

from kivy.vector import Vector
from kivy.clock import Clock
from kivy.properties import NumericProperty
from kivy.uix.stencil import StencilView
from kivy.uix.scatter import ScatterPlane, Scatter


class ScrollPlane(ScatterPlane):
    '''
    ScrollPlane:
    A ScrollPlane is just liek a ScatterPlane, ecept for that its main purpose
    is to scroll through/over its child widgets.  It therefore does not always
    forward motion events directly to it's children.  Instead, if the motion
    event immediately begins with a drag like motion, the ScrollPlane will
    interpret this touch to be used for scrolling instead
    '''

    scroll_init_timeout = NumericProperty(0.2)
    scroll_init_distance = NumericProperty(10)

    def is_scroll_motion(self, touch):
        '''Heuristic for determining if the motion event is used
        for scrolling instead of being handed to child widgets. Called
        for every motion event, until it returns False, after which the
        MotionEvent will start being handed to children.

        :Parameters:
            `touch`: MotionEvent
                motionEvent that is evaluated to determine if the user
                intends to scroll the viewport, or interact with children.
        '''
        if touch.is_double_tab:
            return False

        #if within timelimit, it ever movesfar enough away
        #we lock it and will always ise it to scrooll
        dt = Clock.get_time() - touch.start_time
        if dt < self.scroll_init_timeout:
            dp = Vector(touch.dpos).length()
            touch.ud['scroll_forever'] = dp > self.scroll_init_distance
            return True

        #after timeout, if it didnt move far enough..no longer kist scroll
        return touch.ud['scroll_forever']

    def on_touch_down(self, touch):
        self.scroll_touch_down(touch)

    def on_touch_move(self, touch):
        self.scroll_touch_move(touch)

    def on_touch_up(self, touch):
        self.scroll_touch_up(touch)

    def scroll_touch_down(self, touch):
        touch.grab(self)
        self._touches.append(touch)
        return True

    def scroll_touch_move(self, touch):
        if touch in self._touches and touch.grab_current == self:
            self.transform_with_touch(touch)
        return True

    def scroll_touch_up(self, touch):
        if touch in self._touches and touch.grab_state:
            touch.ungrab(self)
            self._touches.remove(touch)
        return True


class ScrollView(StencilView):
    '''
    ScrollView:
        A ScrollView provides a scrollable/pannable viewport
        which is clipped to the ScrollView's bounding box.
    '''

    def __init__(self, **kwargs):
        self.viewport = ScrollPlane()
        super(ScrollView, self).__init__(**kwargs)
        super(ScrollView, self).add_widget(self.viewport)

        self.viewport.bind(size=self.size)

    def add_widget(self, widget):
        self.viewport.add_widget(widget)

    def remove_widget(self, widget):
        self.viewport.remove_widget(widget)

    def clear_widgets(self):
        self.viewport.clear()

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            return super(ScrollView, self).on_touch_down(touch)

    def on_touch_move(self, touch):
        if self.collide_point(*touch.pos):
            return super(ScrollView, self).on_touch_move(touch)

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            return super(ScrollView, self).on_touch_up(touch)

