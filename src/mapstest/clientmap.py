"""Extends Engine ClientMap to change map text"""

import pygame
from pygame.locals import *
from engine.log import log
import engine.clientmap   
import engine.time as time
import math

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
            "color": (255, 255, 255, 200),
            "bgcolor": (0, 0, 0, 0),
            "bgbordercolor": (0, 0, 0, 0)
            })
    
    def blitMap(self, destImage, offset, sprites):
        """Extend blitMap() to remove sprites with 'visible' == False"""

        # fancy way to iterate over a list and modify it at the same time. This only keeps sprites that evaluate to True
        sprites = list(filter(lambda s: not ('visible' in s and s['visible'] == False), sprites))  

        # render the map as normal
        return super().blitMap(destImage, offset, sprites)

    def blitSpeechText(self, destImage, offset, object):
        """EXTEND blitSpeechText() to add animated text appearance"""

        # if object has speechText and that text should be animated
        if 'speechText' in object and 'speechTextAppearStart' in object:
            now = time.perf_counter()
            # if the text should not be fully shown yet
            if now < object['speechTextAppearEnd']:
                # percentToShow is the value (betwen 0.0 and 1.0) of how far 'now' is between start and end time.
                percentToShow = (now - object['speechTextAppearStart']) / (object['speechTextAppearEnd'] - object['speechTextAppearStart'])

                # find how many of the total number of letters to show.
                lettersToShow = math.ceil(len(object['speechText']) * percentToShow)

                # truncate speechText to the correct number of letters and render it.
                orig = object['speechText']
                object['speechText'] = object['speechText'][:lettersToShow]
                validUntil1 = super().blitSpeechText(destImage, offset, object)
                # put back the full text so we can use it on the next screen update.
                # we need to put this back since the next letter may need to be displayed before the server sends a new step.
                object['speechText'] = orig

                # at what time should the next letter appear. This is how long the updated display is valid until.
                validUntil2 = now + (object['speechTextAppearEnd'] - object['speechTextAppearStart']) / len(object['speechText'])

                # return min of the two times the screen might need to be updated again.
                return min(validUntil1, validUntil2)

        return super().blitSpeechText(destImage, offset, object)