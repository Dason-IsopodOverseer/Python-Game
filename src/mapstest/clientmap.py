"""Extends Demo ClientMap to format dialog"""

import pygame
from pygame.locals import *

from engine.log import log
import demo.clientmap


class ClientMap(demo.clientmap.ClientMap):
    """Extends demo.clientmap.ClientMap

    This class makes the map render as black except where players
    are standing. Where players are standing it is as if they are
    holding a lantern, brighter closer to the player.
    """

    def __init__(self, tilesets, mapDir):
        """Extends ___init__ and sets up darkness and light circle."""

        super().__init__(tilesets, mapDir)

        self['LIGHTRADIUS'] = 180

        # allocate darknessImage
        self['darknessImage'] = pygame.Surface(
            (self['width'] * self['tilewidth'], self['height'] * self['tileheight']),
            pygame.SRCALPHA,
            32)
        self['darknessImage'] = self['darknessImage'].convert_alpha()

        # allocate and draw lightCircleImage
        self['lightCircleImage'] = pygame.Surface(
            (self['LIGHTRADIUS'] * 2, self['LIGHTRADIUS'] * 2), pygame.SRCALPHA, 32)
        self['lightCircleImage'] = self['lightCircleImage'].convert_alpha()
        self['lightCircleImage'].fill((0, 0, 0, 0))
        for i in range(255, 0, -5):
            pygame.draw.circle(
                self['lightCircleImage'],
                color=(0, 0, 0, 255 - i),  # set the pixel values to subtract during blitMap() below.
                center=(self['LIGHTRADIUS'], self['LIGHTRADIUS']),
                radius=i / 255.0 * self['LIGHTRADIUS']
                )
