import pygame
from pygame.locals import *
import math

from engine.log import log
import engine.client


class Client(engine.client.Client):
    def processEvent(self, event):
        """Extend processEvent()
        Add game specific events for:
            ready (any key) and quit during the pre-game
            fire (f) and run (r) during game. Pass all other events to super()
        """
        if event.type == pygame.TEXTINPUT:
            if event.text == '1':
                self['socket'].sendMessage({'type': '1'})
            if event.text == '2':
                self['socket'].sendMessage({'type': '2'})
            else:
                super().processEvent(event)
        else:
            super().processEvent(event)