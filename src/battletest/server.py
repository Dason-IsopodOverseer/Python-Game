import sys
import random

import engine.time as time
from engine.log import log
import engine.server
import engine.geometry as geo


class Server(engine.server.Server):
    def msg1(self, ip, port, ipport, msg):
        sprite = self['players'][ipport]['sprite']
        if 'action' in sprite:
            sprite['action']['1'] = True
    
    def msg2(self, ip, port, ipport, msg):
        sprite = self['players'][ipport]['sprite']
        if 'action' in sprite:
            sprite['action']['2'] = True