from engine.log import log
import mapstest.servermap
import engine.geometry as geo

rVictory = False

class ServerMap(mapstest.servermap.ServerMap):  
    def triggerRespawn(self, trigger, sprite):
        if(sprite['name'] == "savior"):
            self.rVictory = True
        if(self.rVictory) and (sprite['name'] != "savior"):
            self.setObjectLocationByAnchor(sprite, 370, 150)
