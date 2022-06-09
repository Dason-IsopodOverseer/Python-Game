# import all libraries
import engine.servermap
import json
import os
from ctypes import windll
import engine.geometry as geo
import engine.client

from socketserver import ThreadingUDPServer
from engine.log import log
import engine.stepmap
import engine.time as time
import random

import pygame

class ServerMap(engine.servermap.ServerMap):

    """Extends engine.servermap.ServerMap
    TRIGGER DIALOG MECHANIC
        Allows cutscenes with text to be shown. Text can be advanced by player input (currently only spacebar at the moment.
    
    LOADING DIALOG JSON FILES
        Loads strings of text stored as a json file
    
    LOADING MUSIC AND SOUND FILES
        Loads music and plays them, can also be triggered by cutscene
    """
    
    # GLOBAL CLASS VARIABLES
    # dialog
    dialog1 = "empty" #do not alter this under any circumstance
    inDialog = False # true if the characters are in dialog
    dialogCounter = 0 # incrementer used to prgress dialog
    dialogComplete = [] # prevents idalog from re-triggering on same map
    canMove = True # used to enable and disable mouse click
    currentSpeaker = "Eric" # used to store current player
    enemySpeaker = False # true if the current speaker is an enemy
    currentMusic = ""

    # battle
    battleEnded = False
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

    attackOption = 0

    # loads a json file
    def getFilePath(self, folderName, fileName, fileExtension):
        # find json file by formatting the name exactly
        dir_name = os.path.dirname(os.path.realpath(__file__))
        base_filename = fileName
        folder = folderName
        filename_suffix = fileExtension
        parent_path = os.path.join(dir_name, folder)
        filepath = os.path.join(parent_path, base_filename + "." + filename_suffix)
        return filepath
    
    # initializes all class variables essential for cutscene dialogs
    def initDialogs(self):
        filepath = self.getFilePath("dialog", "1", "json")
        if os.path.isfile(filepath):
            print("file found")
        else: 
            print("dialog json file error.")
            quit()
        # Opening JSON file
        with open(filepath) as f:
            self.dialog1 = json.load(f)
        # Prepare the array which counts dialog completion
        self.dialogComplete = []
        for i in self.dialog1:
            self.dialogComplete.append(False)
    
    # loads pygame to prepare music files
    def initMusic(self):
        pygame.init()

    def freeze(self, sprite):
        print("freeze triggered")      
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

    # this function continuously runs, making the cutscene work
    def triggerCutscene(self, trigger, sprite):
        id = trigger['prop-id']
        if (self.inDialog):
            name = sprite["name"]
            if (name == self.currentSpeaker):
                self.speak(sprite, id)
                if "action" in sprite:
                    self.dialogCounter += 1
            if (self.enemySpeaker):
                if "action" in sprite:
                    self.dialogCounter += 1
    
    # sound can be triggered as part of a cutscene
    def playSound(self, name, extension):
        filepath = self.getFilePath("sounds", name, extension)
        soundObj = pygame.mixer.Sound(filepath)
        soundObj.play()

    # music can be triggered as part of a cutscene
    def playMusic(self, name, extension):
        if (self.currentMusic != ""):
            self.currentMusic.stop()
        filepath = self.getFilePath("music", name, extension)
        soundObj = pygame.mixer.Sound(filepath)
        self.currentMusic = soundObj
        soundObj.play(-1)
    
    def stopMusic(self):
        self.currentMusic.stop()
        self.currentMusic = ""

    # this function is fired whenever a player steps onto a dialog box
    def triggerDialog(self, trigger, sprite):
        id = trigger['prop-id']
        if not self.dialogComplete[id]:
            self.setMoveLinear(sprite, sprite['anchorX'], sprite['anchorY'], 100)
            self.inDialog = True
            self.dialogComplete[id] = True
    
    # corollary function. Does the same thing as trigger Dialog, but only IF a specific sprite steps on it
    # AND it is currently their turn
    def triggerSpecificdialog(self, trigger, sprite):
        name = sprite["name"]
        if (name == trigger['prop-name']) and (self.currentSpeaker == name):
            self.triggerDialog(trigger, sprite)
    
    # corollary function. Does the same thing as trigger Dialog, but SETS THE CURRENT TURN TO THE SPRITE WHO FIRST HITS IT
    def triggerSelfdialog(self, trigger, sprite):
        id = trigger['prop-id']
        if not self.dialogComplete[id]:
            name = sprite["name"]
            self.currentSpeaker = name
        self.triggerDialog(trigger, sprite)

    def finishBattleDialog(self):
        self.currentSpeaker = "Eric"

    """counts the dialog progression and executes dialog.
    dialog is complete when all lines in the array have been said, so dialogcounter == array.length"""
    def speak(self, sprite, id):
        text = []
        for i in self.dialog1[str(id)]:
            text.append(i)
        t = text[self.dialogCounter]
        if (self.dialogCounter >= len(text) - 1) or ("end%" in t): 
            self.enemySpeaker = False
            self.inDialog = False
            self.dialogCounter = 0
            self.setSpriteSpeechText(sprite, "end of message") #won't actually show up, btw. Just a placeholder to be removed
            self.delSpriteSpeechText(sprite)
        elif("move%" in t):
            t = t.split(" ")
            self.setMoveLinear(sprite, int(t[1]), int(t[2]), int(t[3]))
            self.dialogCounter += 1
        elif ("speaker%" in t):
            t = t.split(" ")
            if t[1] != "Eric" and t[1] != "Andre" and t[1] != "Leslie":
                self.enemySpeaker = True
            else:
                self.enemySpeaker = False
            self.currentSpeaker = t[1]
            self.dialogCounter += 1
        elif("unlock%" in t): 
            self.canMove = True
            self.dialogCounter += 1
        elif("lock%" in t):
            self.canMove = False
            self.dialogCounter += 1
        elif("assemblex%" in t):
            currentX = sprite['anchorX']
            currentY = sprite['anchorY']
            n = 20
            # teleports all players to the current player's location, x-shifted
            for sprite in self['sprites']:
                n = n + 10
                if sprite['type'] == "player":
                    self.setObjectLocationByAnchor(sprite, currentX + n, currentY)
                    n = n - 30
            n = 0
            self.dialogCounter += 1
        elif("assembley%" in t):
            currentX = sprite['anchorX']
            currentY = sprite['anchorY']
            n = 20
            # teleports all players to the current player's location, y-shifted
            for sprite in self['sprites']:
                n = n + 10
                if sprite['type'] == "player":
                    self.setObjectLocationByAnchor(sprite, currentX, currentY + n)
                    n = n - 30
            n = 0
            self.dialogCounter += 1    
        elif("teleport%" in t):
            t = t.split(" ")
            # teleports the selected player to the specified location
            self.setObjectLocationByAnchor(sprite, int(t[1]), int(t[2]))
            self.dialogCounter += 1     
        elif("sound%" in t):
            t = t.split(" ")
            self.playSound(t[1], t[2])
            self.dialogCounter += 1
        elif("silence%" in t):
            self.stopMusic()
            self.dialogCounter += 1
        elif("music%" in t):
            t = t.split(" ")
            self.playMusic(t[1], t[2])
            self.dialogCounter += 1
        elif("hide%" in t):
            for sprite in self['sprites']:
                if sprite['type'] == 'player' or sprite['type'] == 'enemy':
                    sprite['visible'] = False
            self.dialogCounter += 1
        elif("show%" in t):
            sprite['visible'] = True
            self.dialogCounter += 1
        elif("battle%" in t):
            self.currentSpeaker = "!@$!^!@#" # prevents anyone from speaking
            self.setLayerVisablitybyName("battle", True)
            self.dialogCounter += 1
        elif("battledone%" in t):
            self.setLayerVisablitybyName("battle", False)
            self.dialogCounter += 1
        else:
            self.setSpriteSpeechText(sprite, t)

    def getMovability(self):
        return self.canMove
    
    # start of Emily's code
        ########################################################
    # BATTLE ACTION MECHANIC
    ########################################################

    def attack(self, trigger, sprite):
        #log(self.attackOption)
        if sprite["name"] == "Andre":
            atkArr = self.aAttacks
        elif sprite["name"] == "Eric":
            atkArr = self.eAttacks
        elif sprite["name"] == "Leslie":
            atkArr = self.lAttacks
        damage = random.randrange(8, 12)
        
        if self.attackOption == 1:
            n = random.randrange(1, 20)
            
            damage *= atkArr[0][1]
            if (n > atkArr[0][2]):	
                self.setSpriteSpeechText(sprite, "Attacked!", time.perf_counter() + 2)
                self.enemyHealth -= int(damage)
                if (n == 20):	
                    self.enemyHealth -= random.randrange(3, 7)	
                    self.setSpriteSpeechText(sprite, "Critical hit!", time.perf_counter() + 1)	
            else:
                self.setSpriteSpeechText(sprite, "Oops, that attack whiffed.", time.perf_counter() + 2)
                
            self.attacking = False
            self.delSpriteAction(sprite)
            self.attackOption = 0
            self.advanceTurn()

        elif self.attackOption == 2:
            n = random.randrange(1, 21)
            
            damage *= atkArr[1][1]
            if (n > atkArr[1][2]):	
                self.setSpriteSpeechText(sprite, "Attacked!", time.perf_counter() + 2)
                self.enemyHealth -= int(damage)	
                if (n == 20):	
                    self.enemyHealth -= random.randrange(3, 7)	
                    self.setSpriteSpeechText(sprite, "Critical hit!", time.perf_counter() + 1)	
            else:
                self.setSpriteSpeechText(sprite, "Oops, that attack whiffed.", time.perf_counter() + 2)
                

            self.attacking = False
            self.delSpriteAction(sprite)
            self.attackOption = 0
            self.advanceTurn()

    def act(self, trigger, sprite, currentAct):
        """BATTLE ACTION MECHANIC: act method.

        Upon interacting with a battle action trigger, if the sprite's turn 
        is not currently over and the sprite has requested an action, perform
        action accordingly.
        """
        
        
        if "action" in sprite and not self.turnDone:
            self.delSpriteAction(sprite)
            	
            # if player defending
            if currentAct == 'd':
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

            """
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

            self.advanceTurn()

    def advanceTurn(self):
        self.currentTurn += 1
        if self.currentTurn > 2:
                self.currentTurn = 0
                self.turnDone = True
        while (self.currentTurn == 0 and "Eric" not in self.players) or (self.currentTurn == 1 and "Andre" not in self.players) or (self.currentTurn == 2 and "Leslie" not in self.players):
            self.currentTurn += 1
            if self.currentTurn > 2:
                self.currentTurn = 0
                self.turnDone = True

    def triggerAttack(self, trigger, sprite):
        """BATTLE ACTION MECHANIC: triggerAttack method.

        Prompt player to attack and perform attack if sprite requests action.
        """
        if not self.turnDone:
            if (self.currentTurn == 0 and sprite["name"] == "Eric") or (self.currentTurn == 1 and sprite["name"] == "Andre") or (self.currentTurn == 2 and sprite["name"] == "Leslie"):
                self.setSpriteSpeechText(sprite, "Press space to attack")
                if sprite["name"] == "Andre":
                    atkArr = self.aAttacks
                elif sprite["name"] == "Eric":
                    atkArr = self.eAttacks
                elif sprite["name"] == "Leslie":
                    atkArr = self.lAttacks

                if "action" in sprite:
                    self.attacking = True
                    self.attackOption = 0
                if self.attacking:
                    self.setSpriteSpeechText(sprite, "Select an attack: \n1. " + atkArr[0][0] + "\n2. " + atkArr[1][0])
                    self.attack(self, sprite)

    
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
    
    def setAtkOption(self, sprite, opt):
        self.attackOption = opt
        #log("ok")
    
    ########################################################
    # TURN MECHANIC
    ########################################################

    def stepMapStartBattle(self):
        for sprite in self['sprites']:
            if sprite['type'] == "enemy":
                if self.enemyHealth <= 0:
                    if not self.battleEnded:
                        self.currentSpeaker = "Eric"
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
                                
                                self.players[target] -= int(damage)
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

    ########################################################
    # TYPE WRITER MECHANIC
    ########################################################
    def setSpriteSpeechText(self, sprite, speechText, speechTextDelAfter=0, speechTextAppearSec = 0.5):
        """EXTEND setSpriteSpeechText() to add animated text appearance"""
        speechTextAppearSec = (len(speechText))/30
        super().setSpriteSpeechText(sprite, speechText, speechTextDelAfter)

        # if a speechTextAppearSec has been provided and a start time is not already in sprite
        if speechTextAppearSec > 0 and 'speechTextAppearStart' not in sprite:
                # add time to start and end appearance of text.
                now = time.perf_counter()
                # start showing text at this time
                sprite['speechTextAppearStart'] = now
                # text should be fully shown by this time.
                sprite['speechTextAppearEnd'] = now + speechTextAppearSec