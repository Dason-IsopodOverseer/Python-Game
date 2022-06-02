from socketserver import ThreadingUDPServer
import engine.servermap
from engine.log import log
import engine.stepmap
import engine.time as time

class ServerMap(engine.servermap.ServerMap):
    """Extends engine.servermap.ServerMap

    This class implements mechanics:

    BATTLE ACTION MECHANIC
        Allow player to perform battle actions (attack, defend, and special
        action) when in a trigger of type attack, defend, or special.

        Uses mechanics: action, speech text
    
    CURSOR SPRITE MECHANIC - TO IMPLEMENT
        Player's sprite is changed to a cursor, which moves at a faster speed
    
    TURN MECHANIC - TO IMPLEMENT
        Allows player(s) and enemy to alternate turns in battle.
    """
    turnDone = False
    eTurnEndTime = 0

    ########################################################
    # BATTLE ACTION MECHANIC
    ########################################################

    def act(self, trigger, sprite, currentAct):
        """BATTLE ACTION MECHANIC: act method.

        Upon interacting with a battle action trigger, if the sprite's turn 
        is not currently over and the sprite has requested an action, perform
        action accordingly.
        """
        if "action" in sprite and not self.turnDone:
            self.delSpriteAction(sprite)
            if currentAct == 'a':
                self.setSpriteSpeechText(sprite, "attacked", time.perf_counter() + 2)
            elif currentAct == 'd':
                self.setSpriteSpeechText(sprite, "defended", time.perf_counter() + 2)
            elif currentAct == 's':
                self.setSpriteSpeechText(sprite, "acted specially", time.perf_counter() + 2)
            self.turnDone = True

    def triggerAttack(self, trigger, sprite):
        """BATTLE ACTION MECHANIC: triggerAttack method.

        Prompt player to attack and perform attack if sprite requests action.
        """
        if not self.turnDone:
            self.setSpriteSpeechText(sprite, "Press space to attack")
            self.act(self, sprite, 'a')

    def triggerDefend(self, trigger, sprite):
        """BATTLE ACTION MECHANIC: triggerDefend method.

        Prompt player to defend and perform defense if sprite requests action.
        """
        if not self.turnDone:
            self.setSpriteSpeechText(sprite, "Press space to defend")
            self.act(self, sprite, 'd')
    
    def triggerSpecial(self, trigger, sprite):
        """BATTLE ACTION MECHANIC: triggerSpecial method.

        Prompt player to use special action and perform special action if sprite 
        requests action.
        """
        if not self.turnDone:
            self.setSpriteSpeechText(sprite, "Press space to use special action")
            self.act(self, sprite, 's')
    
    ########################################################
    # TURN MECHANIC
    ########################################################
    def stepMapStartEnemy(self):
        for sprite in self['sprites']:
            if sprite['name'] == "enemy":
                if self.turnDone:
                    #text now working, only disappears if player sprite is moving (?)
                    self.setSpriteSpeechText(sprite, "he he he haw", time.perf_counter() + 0.1)

                    if self.eTurnEndTime == 0:
                        self.eTurnEndTime = time.perf_counter() + 2
                    elif time.perf_counter() > self.eTurnEndTime:
                        self.eTurnEndTime = 0
                        self.turnDone = False
                       
                    