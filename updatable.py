import pdb

class Updatable:
    
    update_list = []
    
    @staticmethod
    def updateAll(dt):
        for thingy in Updatable.update_list:
            thingy.update(dt)
    
    def __init__(self):
        Updatable.update_list.append(self)
        self.updating = True
        
    def update(self, dt):
        pass
    
    def ignoreUpdates(self):
        '''Stop this object from having its update method called each frame.'''
        if self.updating:
            self.updating = False
            Updatable.update_list.remove(self)
            
    def resumeUpdates(self):
        '''Make this object receive update calls each frame again if it was previously ignoring them.'''
        if not self.updating:
            self.updating = True
            Updatable.update_list.append(self)
