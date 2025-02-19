"""Extends Engine ClientMap to change map text"""

import pygame
from pygame.locals import *
from engine.log import log
import engine.clientmap
class ClientMap(engine.clientmap.ClientMap):
    """Extends engine.clientmap.ClientMap"""

    def __init__(self, tilesets, mapDir):
        """Extends ___init__ and updates text defaults."""

        super().__init__(tilesets, mapDir)

        # defaults for map text
        self['DEFAULTTEXT'].update({
            'pixelsize': 15,
            "color": (0, 0, 0, 255),
            "bgcolor": (255, 255, 255, 150),
            "halign": "center",
            "bgbordercolor": (0, 0, 0, 150),
            "bgborderThickness": 1,
            "bgroundCorners": 5
            })

        # labelText defaults that differ from DEFAULTTEXT
        self['LABELTEXT'].update({
            'pixelsize': 12,
            "color": (0, 0, 0, 200),
            "bgcolor": (0, 0, 0, 0),
            "bgbordercolor": (0, 0, 0, 0)
            })

