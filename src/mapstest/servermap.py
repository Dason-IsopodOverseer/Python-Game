import engine.servermap
import json
import os
from ctypes import windll
import engine.geometry as geo
import engine.client

class ServerMap(engine.servermap.ServerMap):

    """Extends engine.servermap.ServerMap

    TRIGGER DIALOG MECHANIC
        Allows cutscenes with text to be shown. Text can be advanced by player input (currently only spacebar at the moment, 
        I don't know how to get  anything else).
    
    LOADING DIALOG JSON FILES
        Loads strings of text stored as a json file
    """
    
    # GLOBAL CLASS VARIABLES
    dialog1 = "empty" #do not alter this under any circumstance
    inDialog = False
    dialogCounter = 0
    dialogComplete = []
    dialogCompleteCounter = 0
    canMove = True # used to enable and disable mouse click
    currentSpeaker = "Eric"

    # loads a json file
    def getJsonPath(self, folderName, fileName):
        # find json file by formatting the name exactly
        dir_name = os.path.dirname(os.path.realpath(__file__))
        base_filename = fileName
        folder = folderName
        filename_suffix = "json"
        parent_path = os.path.join(dir_name, folder)
        filepath = os.path.join(parent_path, base_filename + "." + filename_suffix)
        print("Loading json using the following path: " + filepath)
        return filepath

    # initializes all class variables essential for cutscene dialogs
    def initDialogs(self):
        filepath = self.getJsonPath("dialog", "1")
        if os.path.isfile(filepath):
            print("file found")
        else: 
            print("dialog josn file error.")
            quit()
        # Opening JSON file
        with open(filepath) as f:
            self.dialog1 = json.load(f)
        # Prepare the array which counts dialog completion
        self.dialogComplete = []
        for i in self.dialog1:
            self.dialogComplete.append(False)
    
    """
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
    """

    # this function continuously runs, making the cutscene work
    def triggerCutscene(self, trigger, sprite):
        if (self.inDialog):
            name = sprite["name"]
            if (name == self.currentSpeaker):
                self.speak(sprite, self.dialogCompleteCounter)
                if "action" in sprite:
                    self.dialogCounter += 1
    
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

    """counts the dialog progression and executes dialog.
    dialog is complete when all lines in the array have been said, so dialogcounter == array.length"""
    def speak(self, sprite, id):
        text = []
        for i in self.dialog1[str(id)]:
            text.append(i)
        t = text[self.dialogCounter]
        if (self.dialogCounter >= len(text) - 1) or ("end%" in t): 
            self.inDialog = False
            self.dialogCompleteCounter += 1
            self.dialogCounter = 0
            self.setSpriteSpeechText(sprite, "end of message") #won't actually show up, btw. Just a placeholder to be removed
            self.delSpriteSpeechText(sprite)
        elif("move%" in t):
            t = t.split(" ")
            self.setMoveLinear(sprite, int(t[1]), int(t[2]), int(t[3]))
            self.dialogCounter += 1
        elif ("speaker%" in t):
            t = t.split(" ")
            self.currentSpeaker = t[1]
            self.dialogCounter += 1
        elif("unlock%" in t): 
            self.canMove = True
            self.dialogCounter += 1
        elif("lock%" in t):
            self.canMove = False
            self.dialogCounter += 1
        else:
            self.setSpriteSpeechText(sprite, t)

    def getMovability(self):
        return self.canMove