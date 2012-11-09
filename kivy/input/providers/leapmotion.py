'''
Leap Motion provider implementation
=============================
'''

__all__ = ('LeapMotionEventProvider', )

#from kivy.base import EventLoop
#from collections import deque
from kivy.logger import Logger
from kivy.input.provider import MotionEventProvider
from kivy.input.factory import MotionEventFactory
from kivy.input.motionevent import MotionEvent
import Leap


class LeapMotionEvent(MotionEvent):

    def depack(self, args):
        super(LeapMotionEvent, self).depack(args)


class LeapMotionEventProvider(MotionEventProvider):
    __handlers__ = {}

    def __init__(self, device, args):
        super(LeapMotionEventProvider, self).__init__(device, args)

    #def _run_leap_listener(self, **kwargs):
    #    queue = kwargs.get('queue')
    #    input_fn = kwargs.get('input_fn')
    #    controller = Leap.Controller(self)

    def start(self):
        if self.input_fn is None:
            return
        self.uid = 0
        #self.queue = collections.deque()
        #self.thread = threading.Thread(
        #    target = self._run_leap_listener,
        #    kwargs = {'queue': self.queue, 'input_fn': self.input_fn}
        #)
        #self.thread.daemon = True
        #self.thread.start()
        self.leap_listener = LeapMotionListener(self)
        self.leap_controller = Leap.Controller(self.leap_listener)

    def stop(self):
        super(LeapMotionEventProvider, self).stop()

    def update(self, dispatch_fn):
        pass


class LeapMotionListener(Leap.Listener):

    def __init__(self, leap_provider):
        self._provider = leap_provider

    def onInit(self, controller):
        Logger.debug("leapmotion: Initialized")

    def onConnect(self, controller):
        Logger.debug("leapmotion: Connected")

    def onDisconnect(self, controller):
        Logger.debug("leapmotion: Disconnected")

    def onFrame(self, controller):
        Logger.debug("leapmotion: OnFrame")
        frame = controller.frame()
        hands = frame.hands()
        numHands = len(hands)
        Logger.info("Frame: {0}, hands: {1}".format(frame.id(), numHands))


# registers
MotionEventFactory.register('leapmotion', LeapMotionEventProvider)
