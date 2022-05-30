from socketserver import ThreadingUDPServer
import engine.servermap
from engine.log import log
import engine.stepmap
import engine.time as time
import random

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
    enemyHealth = 100
    eHealth = 30
    aHealth = 40
    lHealth = 25
    enemyDmgMult = 1
    eDefending = False
    aDefending = False
    lDefending = False
    aDmgMult = 1.2
    eDmgMult = 1
    lDmgMult = 0.9
    aDefMult = .75
    eDefMult = .70
    lDefMult = .60
    enAttacked = False
    currentTurn = 0

    def getMovability(self):
        return True

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

            # if player attacking
            if currentAct == 'a':
                damage = random.randrange(8, 12)

                if (sprite["name"] == "Andre"):
                    damage *= self.aDmgMult
                elif (sprite["name"] == "Eric"):
                    damage *= self.eDmgMult
                elif (sprite["name"] == "Leslie"):
                    damage *= self.lDmgMult

                self.setSpriteSpeechText(sprite, "attacked", time.perf_counter() + 2)
                
                n = random.randrange(1, 20)
                if (n > 3):
                    self.enemyHealth -= damage
                    if (n == 20):
                        self.enemyHealth -= random.randRange(5, 7)
                        self.setSpriteSpeechText(sprite, "critical hit!", time.perf_counter() + 1)
            
            # if player defending
            elif currentAct == 'd':
                self.setSpriteSpeechText(sprite, "defended", time.perf_counter() + 2)
                if (sprite["name"] == "Andre"):
                    self.aDefending = True
                elif (sprite["name"] == "Eric"):
                    self.eDefending = True
                elif (sprite["name"] == "Leslie"):
                    self.lDefending = True

            # if player using special action
            elif currentAct == 's':
                self.setSpriteSpeechText(sprite, "acted specially", time.perf_counter() + 2)
        self.currentTurn += 1
        if self.currentTurn > 2:
            self.currentTurn = 0
            self.turnDone = True

    def triggerAttack(self, trigger, sprite):
        """BATTLE ACTION MECHANIC: triggerAttack method.

        Prompt player to attack and perform attack if sprite requests action.
        """
        if not self.turnDone:
            #if (self.currentTurn == 0 and sprite["name"] == "Eric") or (self.currentTurn == 1 and sprite["name"] == "Andre") or (self.currentTurn == 2 and sprite["name"] == "Leslie"):
                self.setSpriteSpeechText(sprite, "Press space to attack")
                self.act(self, sprite, 'a')

    
    def triggerDefend(self, trigger, sprite):
        """BATTLE ACTION MECHANIC: triggerDefend method.

        Prompt player to defend and perform defense if sprite requests action.
        """
        if not self.turnDone:
            #if (self.currentTurn == 0 and sprite["name"] == "Eric") or (self.currentTurn == 1 and sprite["name"] == "Andre") or (self.currentTurn == 2 and sprite["name"] == "Leslie"):
                self.setSpriteSpeechText(sprite, "Press space to defend")
                self.act(self, sprite, 'd')
    
    def triggerSpecial(self, trigger, sprite):
        """BATTLE ACTION MECHANIC: triggerSpecial method.

        Prompt player to use special action and perform special action if sprite 
        requests action.
        """
        if not self.turnDone:
            #if (self.currentTurn == 0 and sprite["name"] == "Eric") or (self.currentTurn == 1 and sprite["name"] == "Andre") or (self.currentTurn == 2 and sprite["name"] == "Leslie"):
                self.setSpriteSpeechText(sprite, "Press space to use special action")
                self.act(self, sprite, 's')
    
    ########################################################
    # TURN MECHANIC
    ########################################################
    def stepMapStartBattle(self): #was stepMapStartEnemy
        for sprite in self['sprites']:
            if sprite['name'] == "enemy":
                self.setSpriteLabelText(sprite, "health: " + str(self.enemyHealth))
                if self.turnDone:
                    #text now working, only disappears if player sprite is moving (?)
                    self.setSpriteSpeechText(sprite, "he he he haw", time.perf_counter() + 0.1)
                    
                    if self.eTurnEndTime == 0:
                        self.eTurnEndTime = time.perf_counter() + 2

                    # if enemy's turn is done
                    elif time.perf_counter() > self.eTurnEndTime:
                        if not self.enAttacked:
                            x = random.randrange(0, 2) #determining target of attack
                            damage = random.randrange(5, 7)*self.enemyDmgMult
                            if (x == 0): # eric attacked
                                if self.eDefending:
                                    damage *= self.eDefMult
                                self.eHealth -= damage
                            elif (x == 1): # andre attacked
                                if self.aDefending:
                                    damage *= self.aDefMult
                                self.aHealth -= damage
                            elif (x == 1): # leslie attacked
                                if self.lDefending:
                                    damage *= self.lDefMult
                                self.aHealth -= damage
                        
                        
                        # reset all the stuff
                        self.enAttacked = True
                        self.eTurnEndTime = 0
                        self.turnDone = False
                        self.enAttacked = False
                        self.eDefending = False
                        self.aDefending = False
                        self.lDefending = False

            elif sprite['name'] == "Eric":
                self.setSpriteLabelText(sprite, "health: " + str(self.eHealth))
            elif sprite['name'] == "Andre":
                self.setSpriteLabelText(sprite, "Health: " + str(self.aHealth))
            elif sprite['name'] == "Leslie":
                self.setSpriteLabelText(sprite, "Health: " + str(self.lHealth)) 
                    