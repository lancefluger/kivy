'''
Leap Motion provider implementation
=============================
'''

__all__ = ('LeapMotionEventProvider', )

#from kivy.base import EventLoop
from collections import deque
from kivy.logger import Logger
from kivy.input.provider import MotionEventProvider
from kivy.input.factory import MotionEventFactory
from kivy.input.motionevent import MotionEvent
import Leap

_LEAP_QUEUE = deque()


class LeapMotionEvent(MotionEvent):

    def depack(self, args):
        super(LeapMotionEvent, self).depack(args)
        if args[0] is None:
            return
        self.profile = ('hand', 'fingers', 'palm')
        hand = args[0]
        self.fingers = hand.fingers()
        self.palm = None
        palmRay = hand.palm()
        if palmRay is not None:
            self.palm = palmRay.position
            #wrist = palmRay.direction
            #direction = "right"
            #if wrist.x > 0:
            #    direction = "left"
            self.sx = self.palm.x
            self.sy = self.palm.y
            self.sz = self.palm.z


class LeapMotionEventProvider(MotionEventProvider):
    __handlers__ = {}

    def __init__(self, device, args):
        super(LeapMotionEventProvider, self).__init__(device, args)

    def start(self):
        self.uid = 0
        self.current_hands = []
        self.listener = LeapMotionListener()
        self.controller = Leap.Controller(self.listener)

    def stop(self):
        super(LeapMotionEventProvider, self).stop()

    def update(self, dispatch_fn):
        try:
            while True:
                frame = _LEAP_QUEUE.popleft()
                events = self.process_frame(frame)
                for ev in events:
                    dispatch_fn(*ev)
        except IndexError:
            pass

    def process_frame(self, frame):
        old_hands = self.current_hands
        new_hands = []
        events = []
        for hand in frame.hands():
            hid = hand.id()
            new_hands.append(hid)
            if hid in old_hands:
                ev_type = 'move'
                old_hands.remove(hid)
            else:
                ev_type = 'down'
            ev = (ev_type, LeapMotionEvent(self.device, hid, [hand]))
            events.append(ev)
        self.current_hands = new_hands
        for hid in old_hands:
            ev = ('up', LeapMotionEvent(self.device, hid, [None]))
        return events


class LeapMotionListener(Leap.Listener):

    def onInit(self, controller):
        Logger.info("leapmotion: Initialized")

    def onConnect(self, controller):
        Logger.info("leapmotion: Connected")

    def onDisconnect(self, controller):
        Logger.info("leapmotion: Disconnected")

    def onFrame(self, controller):
        Logger.trace("leapmotion: OnFrame")
        frame = controller.frame()
        _LEAP_QUEUE.append(frame)


# registers
MotionEventFactory.register('leapmotion', LeapMotionEventProvider)
