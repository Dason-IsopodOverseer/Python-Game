"""Client for Demo Game"""

import pygame
from pygame.locals import *

from engine.log import log
import engine.client


class Client(engine.client.Client):
    """Extends engine.client"""