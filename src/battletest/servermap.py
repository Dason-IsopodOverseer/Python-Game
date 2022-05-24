import engine.servermap

class ServerMap(engine.servermap.ServerMap):
    def triggerSayhello(self, trigger, sprite):
        self.setSpriteSpeechText(sprite, f"Hello World")
    
    def triggerAttack(self, trigger, sprite):
        self.setSpriteSpeechText(sprite, "Press space to attack")
    
    def triggerDefend(self, trigger, sprite):
        self.setSpriteSpeechText(sprite, "Press space to defend")
    
    def triggerSpecial(self, trigger, sprite):
        self.setSpriteSpeechText(sprite, "Press space to use special action")