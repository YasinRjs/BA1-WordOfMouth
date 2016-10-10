from Person import *
from PlatformUtils import *
from tkinter.colorchooser import *

from tkinter import *
from tkinter.messagebox import *
from random import random,randint

#Classe qui va créer mon Canvas via le RadioButton du GUI
#Soit circulaire soit Rectangulaire
class NetworkFrame(Canvas):
  """
  Classe qui encapsule le Canvas.
  Possède 2 differents layout Circulaire/Random
  """
  CANVASWEIGHT = 900
  CANVASHEIGHT = 400
  NEWUSER = "#A00000"
  def __init__(self,parent,displayCircular,w=CANVASWEIGHT,h=CANVASHEIGHT):
    Canvas.__init__(self,parent,width=w,height=h)
    self.parent = parent
    self.display = displayCircular 
    self.middle = (self.CANVASWEIGHT/2,self.CANVASHEIGHT/2)   # Milieu du canvas
    self.upLine = 50               # Ligne supérieur pour le random
    self.downLine = 300            # Ligne inférieur 
    self.randomList = []
    
  #Ajoute un oval representant un noeud sur le canvas
  def addDisplay(self,other):
    """
    Place les noeuds par rapport au layout selectionné
    """
    frame = other.networkFrame
    r = other.allNode[0].width
    userNumber = len(other.allNode)
    for i in range(userNumber):
      person = other.allNode[i]
      if other.circulairDisplay:
        x = self.CANVASWEIGHT/2 - ((self.CANVASWEIGHT-r*4)/2 * cos((i*(360/userNumber)) * pi/180))
        y = self.CANVASHEIGHT/2 + ((self.CANVASHEIGHT-r*4)/2 * sin((i*(360/userNumber)) * pi/180))
      else:
        x = self.randomList[i][0]
        y = self.randomList[i][1]
      person.middle = (x,y)
      person.x0 = x-r
      person.y0 = y-r
      person.x1 = x+r
      person.y1 = y+r
      person.oval = frame.create_oval(x-r,y-r,x+r,y+r,fill=person.rumor,\
      width=person.dashWIDTH,outline=person.outline,dash=person.dash)
      frame.tag_bind(person.oval,"<Motion>",other.enterItem)
      frame.tag_bind(person.oval,"<Leave>",other.leaveItem)
      frame.tag_bind(person.oval,"<Double-Button-1>",other.removeNode)
    if other.circulairDisplay and userNumber <= 30:
      other.addNamesOnCanvas()

  def doRandomList(self,other):
    self.randomList = [(randint(20,self.CANVASWEIGHT-30),randint(20,self.CANVASHEIGHT-30))\
      for i in range(len(other.allNode))]
