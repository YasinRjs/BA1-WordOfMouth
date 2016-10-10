from Link import *
from math import sin,cos,pi

class Person:
  """
  Classe graphique Person.
  Une personne est representé par un noeud et un oval sur le canvas
  Chaque noeud possède une couleur(rumor) et une liste d'amis personnel
  """
  DASHWIDTH = 3
  DIVNODEWIDTH = 10
  BASENODEWIDTH = 15
  BLACK = "#000000"

  def __init__(self,name,width):
    self.name = name
    self.width = self.BASENODEWIDTH + width/self.DIVNODEWIDTH
    self.rumor = self.BLACK         # La rumeur est la coleur interne
    self.middle = 0
    self.dash = None
    self.dashWIDTH = self.DASHWIDTH
    self.outline = self.BLACK
    self.friends = []              # Liste regroupant les amis de la personne
    self.oldFriends = []
    self.oldRumors = []
    self.cluedoSuspect = None
    self.cluedoArme = None
    self.cluedoLieu = None
    self.cluedoRumor = "Doesn't know the rumor"

  def friendsLink(self,other):
    """
    Trace les liens d'amitié de la personne sur le canvas
    """
    self.links = Link(other,self)

  def knowsRumor(self):
    """
    Renvoie un booléen True si la personne connait la rumeur
    """
    return self.rumor != self.BLACK
