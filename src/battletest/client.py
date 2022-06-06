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
        if self['ready'] == False:
            if event.type == QUIT:
                quit()
            elif event.type == pygame.TEXTINPUT:
                self['socket'].sendRecvMessage({'type': 'readyRequest'})
                self['ready'] = True
                log("Player Ready.")
        else:
            if event.type == pygame.TEXTINPUT:
                if event.text == 'r':
                    self['socket'].sendMessage({'type': 'run'})
                elif event.text == 'f':
                    fireDestX, fireDestY = pygame.mouse.get_pos()
                    fireDestX -= self['mapOffset'][0]
                    fireDestY -= self['mapOffset'][1]
                    self['socket'].sendMessage({
                        'type': 'fire',
                        'fireDestX': fireDestX,
                        'fireDestY': fireDestY
                        })
                else:
                    super().processEvent(event)
            else:
                super().processEvent(event)