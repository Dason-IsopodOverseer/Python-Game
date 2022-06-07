import sys
import random

import engine.time as time
from engine.log import log
import engine.server
import engine.geometry as geo


class Server(engine.server.Server):
    def msg1(self, ip, port, ipport, msg):
        sprite = self['players'][ipport]['sprite']
        map = self['maps'][sprite['mapName']]
        map.setAtkOption(sprite, 1)
    
    def msg2(self, ip, port, ipport, msg):
        sprite = self['players'][ipport]['sprite']
        map = self['maps'][sprite['mapName']]
        map.setAtkOption(sprite, 2)