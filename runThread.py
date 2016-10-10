from threading import Thread
import time

class PropagateThread(Thread):
    """
    Thread pour pouvoir ajouter un délai entre les simulations.
    """
    def __init__(self, gui):
        Thread.__init__(self)
        self.gui = gui
    def run(self):
      # En cas de fermeture de la fenetre principale lors d'un thread
        steps = self.gui.numberOfSteps.get()
        self.gui.steps.destroy()
        self.gui.activeThread = True
        self.gui.startedPropagation = True
        for i in range(steps):
          if i>0:
            time.sleep(self.gui.valueDelay.get())
          self.gui.propagateTheRumor()
          self.gui.stepNumber.set(self.gui.stepNumber.get() + 1)
          self.gui.addNodesOnCanvas()
        self.gui.activeThread = False
