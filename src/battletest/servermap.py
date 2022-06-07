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
    attacking = False
    enemyHealth = 100
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
    players = {
        "Eric" : 30,
        "Andre" : 45,
        "Leslie" : 25
    }
    eAttacks = [
        ["Engineering Aspirations", 1, 3],
        ["Cram Session", 1.5, 8]
    ]

    aAttacks = [
        ["Football", 1.2, 3],
        ["Varsity Athlete Enhancers", 1.4, 5]
    ]

    lAttacks = [
        ["Artistic Talent", 0.8, 3],
        ["Slam Poetry", 1.2, 7]
    ]

    def getMovability(self):
        return True
    ########################################################
    # BATTLE ACTION MECHANIC
    ########################################################

    def attack(self, trigger, sprite):
        if sprite["name"] == "Andre":
            atkArr = self.aAttacks
        elif sprite["name"] == "Eric":
            atkArr = self.eAttacks
        elif sprite["name"] == "Leslie":
            atkArr = self.lAttacks
        if "atkOption" in sprite:
            if sprite["atkOption"] == 1:
                log("hi this is workingngngngngng")
                self.attacking = False
                self.delSpriteAction(sprite)
                self.delSpriteAtk(sprite)
                self.setSpriteSpeechText(sprite, "using attack one!", time.perf_counter() + 2)
    
    def act(self, trigger, sprite, currentAct):
        """BATTLE ACTION MECHANIC: act method.

        Upon interacting with a battle action trigger, if the sprite's turn 
        is not currently over and the sprite has requested an action, perform
        action accordingly.
        """
        
        
        if "action" in sprite and not self.turnDone:
            self.delSpriteAction(sprite)
            
        
            
            """
            if currentAct == 'a':
                damage = random.randrange(8, 12)

                if (sprite["name"] == "Andre"):
                    damage *= self.aDmgMult
                elif (sprite["name"] == "Eric"):
                    damage *= self.eDmgMult
                elif (sprite["name"] == "Leslie"):
                    damage *= self.lDmgMult

                n = random.randrange(1, 20)	
                if (n > 3):	
                    self.setSpriteSpeechText(sprite, "attacked", time.perf_counter() + 2)
                    self.enemyHealth -= damage	
                    if (n == 20):	
                        self.enemyHealth -= random.randRange(5, 7)	
                        self.setSpriteSpeechText(sprite, "critical hit!", time.perf_counter() + 1)	
                else:
                    self.setSpriteSpeechText(sprite, "oops, that attack whiffed.")
            	
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
            while (self.currentTurn == 0 and "Eric" not in self.players) or (self.currentTurn == 1 and "Andre" not in self.players) or (self.currentTurn == 2 and "Leslie" not in self.players):
                self.currentTurn += 1
                if self.currentTurn > 2:
                    self.currentTurn = 0
                    self.turnDone = True
        """

    def triggerAttack(self, trigger, sprite):
        """BATTLE ACTION MECHANIC: triggerAttack method.

        Prompt player to attack and perform attack if sprite requests action.
        """
        if not self.turnDone:
            if (self.currentTurn == 0 and sprite["name"] == "Eric") or (self.currentTurn == 1 and sprite["name"] == "Andre") or (self.currentTurn == 2 and sprite["name"] == "Leslie"):
                self.setSpriteSpeechText(sprite, "Press space to attack")
                if "action" in sprite:
                    self.attacking = True
                    self.attack(self, sprite)
                if self.attacking:
                    self.setSpriteSpeechText(sprite, "1, 2")

    
    def triggerDefend(self, trigger, sprite):
        """BATTLE ACTION MECHANIC: triggerDefend method.

        Prompt player to defend and perform defense if sprite requests action.
        """
        self.attacking = False
        if not self.turnDone:
            if (self.currentTurn == 0 and sprite["name"] == "Eric") or (self.currentTurn == 1 and sprite["name"] == "Andre") or (self.currentTurn == 2 and sprite["name"] == "Leslie"):
                self.setSpriteSpeechText(sprite, "Press space to defend")
                self.act(self, sprite, 'd')
    
    def triggerSpecial(self, trigger, sprite):
        """BATTLE ACTION MECHANIC: triggerSpecial method.

        Prompt player to use special action and perform special action if sprite 
        requests action.
        """
        self.attacking = False
        if not self.turnDone:
            if (self.currentTurn == 0 and sprite["name"] == "Eric") or (self.currentTurn == 1 and sprite["name"] == "Andre") or (self.currentTurn == 2 and sprite["name"] == "Leslie"):
                self.setSpriteSpeechText(sprite, "Press space to use special action")
                self.act(self, sprite, 's')
    
    def delSpriteAtk(self, sprite):
        if "atkOption" in sprite:
            del sprite["atkOption"]
    
    def setAtkOption(self, sprite, opt):
        sprite["atkOption"] = opt
        log("ok")
    
    ########################################################
    # TURN MECHANIC
    ########################################################

    def stepMapStartBattle(self):
        for sprite in self['sprites']:
            if sprite['name'] == "enemy":
                if self.enemyHealth <= 0:
                    self.setSpriteLabelText(sprite, "YAY U WIN :)")
                    self.battleEnded = True
                else:
                    self.setSpriteLabelText(sprite, "health: " + str(self.enemyHealth))
                    if self.turnDone:
                        #text now working, only disappears if player sprite is moving (?)
                        self.setSpriteSpeechText(sprite, "he he he haw", time.perf_counter() + 0.1)

                        if self.eTurnEndTime == 0:
                            self.eTurnEndTime = time.perf_counter() + 2
                        elif time.perf_counter() > self.eTurnEndTime:

                            if not self.enAttacked:
                                x = random.randrange(0, len(self.players)) #determining target of attack
                                damage = random.randrange(5, 7)*self.enemyDmgMult
                                target = list(self.players)[x]
                                if(target == "Eric"): # eric attacked
                                    if self.eDefending:
                                        damage *= self.eDefMult
                                elif (target == "Andre"): # andre attacked
                                    if self.aDefending:
                                        damage *= self.aDefMult
                                elif (target == "Leslie"): # leslie attacked
                                    if self.lDefending:
                                        damage *= self.lDefMult
                                
                                self.players[target] -= damage
                                if self.players[target] <= 0:
                                    del self.players[target]
                                
                                #log(self.players[target] + " targeted")
                            
                            
                            # reset all the stuff
                            self.enAttacked = True
                            self.eTurnEndTime = 0
                            self.turnDone = False
                            self.enAttacked = False
                            self.eDefending = False
                            self.aDefending = False
                            self.lDefending = False

            elif sprite['name'] == "Eric":
                if "Eric" in self.players:
                    self.setSpriteLabelText(sprite, "health: " + str(self.players["Eric"]))
                else:
                    self.setSpriteLabelText(sprite, "x_x")
                    self.freeze(sprite)
            elif sprite['name'] == "Andre":
                if "Andre" in self.players:
                    self.setSpriteLabelText(sprite, "Health: " + str(self.players["Andre"]))
                else:
                    self.setSpriteLabelText(sprite, "x_x")
                    self.freeze(sprite)
            elif sprite['name'] == "Leslie":
                if "Leslie" in self.players:
                    self.setSpriteLabelText(sprite, "Health: " + str(self.players["Leslie"]))
                else:
                    self.setSpriteLabelText(sprite, "x_x")
                    self.freeze(sprite)

    def freeze(self, sprite):      
        #Change the sprite's moveSpeed to zero.
        # if sprite is moving, cancel the movement by setting speed to 0.
        if "move" in sprite and sprite['move']['type'] == "Linear":
            sprite['speedMultiNormalSpeed'] = sprite['move']['s']
            sprite['move']['s'] *= 0
 
    def unfreeze(self, sprite):
        #Reset the sprite's moveSpeed.
        if "speedMultiNormalSpeed" in sprite:
                if "move" in sprite and sprite['move']['type'] == "Linear":
                    sprite['move']['s'] = sprite['speedMultiNormalSpeed']
                del sprite['speedMultiNormalSpeed']