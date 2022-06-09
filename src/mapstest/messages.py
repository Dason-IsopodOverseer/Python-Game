import pygame
from pygame.locals import *

from engine.log import log
import engine.messages


class Messages(engine.messages.Messages):
    """Extends engine.messages.Messages"""

    def __init__(self):
        """Extends ___init__ and new flds and message types."""

        super().__init__()
        self['messageDefinitions']['1'] = {}  
        self['messageDefinitions']['2'] = {}