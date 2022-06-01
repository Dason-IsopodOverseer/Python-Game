import engine.servermap
import json
import os
from ctypes import windll
import engine.geometry as geo

class ServerMap(engine.servermap.ServerMap):
    """Extends engine.servermap.ServerMap

    TRIGGER DIALOG MECHANIC
        Allows cutscenes with text to be shown. Text can be advanced by player input (currently only spacebar at the moment, 
        I don't know how to get  anything else).
    
    FREEZE AND UNFREEZE MECHANIC
        Set speed of character to zero when needed, and unfreeze if required. Used as part of 
        dialog cutscenes.

    LOADING DIALOG JSON FILES
        Loads strings of text stored as a json file
    """

    # GLOBAL CLASS VARIABLES
    dialog1 = "empty" #do not alter this under any circumstance
    inDialog = False
    dialogCounter = 0
    dialogComplete = []
    canMove = True # used to enable and disable mouse click 

    # initializes all class variables essential for cutscene dialogs
    def initDialogs(self):
        # find json file
        dir_name = os.path.dirname(os.path.realpath(__file__))
        base_filename = "1"
        folder = "dialog"
        filename_suffix = "json"
        parent_path = os.path.join(dir_name, folder)
        filepath = os.path.join(parent_path, base_filename + "." + filename_suffix)
        print("Loading dialogs using the following path: " + filepath)

        if os.path.isfile(filepath):
            print("file found!")
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

    def triggerSayhello(self, trigger, sprite):
        self.setSpriteSpeechText(sprite, "I seem to have gotten wet.")
    
    # this function is fired whenever a player steps onto a dialog box
    def triggerDialog(self, trigger, sprite):
        id = trigger['prop-id']
        if not self.dialogComplete[id]:
            self.freeze(sprite)
            if not self.inDialog and (self.dialogCounter == 0):
                self.inDialog = True
            elif not self.inDialog and (self.dialogCounter != 0):
                self.unfreeze(sprite)
                self.dialogCounter = 0
                self.dialogComplete[id] = True
                self.setSpriteSpeechText(sprite, "end of message") #won't actually show up, btw. Just a placeholder to be removed
                self.delSpriteSpeechText(sprite)
            else: 
                self.speak(sprite, id)
                if "action" in sprite:
                    self.dialogCounter += 1

    """counts the dialog progression and executes dialog.
    dialog is complete when all lines in the array have been said, so dialogcounter == array.length"""
    def speak(self, sprite, id):
        text = []
        for i in self.dialog1[str(id + 1)]:
            text.append(i)
        if (self.dialogCounter >= len(text)):
            self.inDialog = False
        elif("move%" in  text[self.dialogCounter]):
            self.inDialog = False
            t = text[self.dialogCounter].split(" ")
            self.setMoveLinear(sprite, int(t[1]), int(t[2]), int(t[3]))
            self.unfreeze(sprite)
            self.dialogCounter = 0
            self.dialogComplete[id] = True
        else: 
            t = text[self.dialogCounter]
            if("unlock%" in t):
                self.canMove = True
                t = t.split("unlock% ")[1]
            elif("lock%" in t):
                self.canMove = False
                t = t.split("lock% ")[1]
            self.setSpriteSpeechText(sprite, t)

    def getMovability(self):
        return self.canMove