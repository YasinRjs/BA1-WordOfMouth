#-*- coding: utf-8 -*-

###########################################
#                                         #
#       Partie 3 : La rumeur court ..     #
#       INFO-F-106 : Projet d'année       #
#         Matricule : 000396506           #
#             Arslan Yasin                #
#                                         #
###########################################

"""
Classe principale GUI .
Encapsule la fenetre principale ainsi que ses fenetres secondaires.
Simule une propagation de rumeur sur un Canvas.
Une personne est representé par un oval et 
la rumeur de la personne est representé par la couleur de son oval.
"""

from tkinter import filedialog
from tkinter.simpledialog import *

from NetworkFrame import *
import rumorFunctions as rF
from runThread import *

class GUI(Frame):
  """
  Classe GUI encapsule la fenêtre principale
  """
  LEFTCLICK = str(PlatformUtils.getLeftButton())
  RIGHTCLICK = str(PlatformUtils.getRightButton())
  baseInfo = "Roll over a node"
  NODELIFT = "dark grey"

  cluedoSuspect = ["Mademoiselle Rose","Colonel Moutarde","Madame Leblanc Révérand Olive","Madame Pervenche","Professeur Violet","Monsieur Yasin","Monsieur Jacky"]
  cluedoArme = ["un Poignard","un Revolver","une Matraque","un Chandelier", "une Corde", "une Clé anglaise", "un Flacon de poison", "un Fer à cheval", "une Hache", "un Haltère", "une Batte de baseball", "un Trophée", "un Tuyau de plomb"]
  cluedoLieu = ["dans la Cuisine", "sur la Terrasse", "dans un Spa", "dans la salle à Manger", "à la Piscine", "au Cinema", "dans le Salon", "dans le Pavillon des invités", "dans le Hall", "dans l'Observatoire"]

  def __init__(self,parent):
    Frame.__init__(self,parent)
    self.parent = parent         # Fenetre principale
    self.parent.title('Social Network')
    self.initial()

 #===================
  def initial(self):
 #===================
    self.grid()
    self.parent.resizable(False,False)
    self.structures()
    self.startCanvas()
    self.frames()
    self.mainWidgets()
    self.events()

  #==================
  def frames(self):
  #==================
    """
    Création de toutes les frames
    """
    self.displayFrame = Frame(self)
    self.widthFrame = Frame(self)
    self.edgeFrame = Frame(self)
    self.delayFrame = Frame(self)
    self.selectionPolicyFrame = Frame(self)
    self.rumorRuleFrame = Frame(self)
    self.spreadFrame = Frame(self)
    self.buttonFrame = Frame(self)
    self.displayTitleFrame = Frame(self)
    self.widthTitleFrame = Frame(self)
    self.edgeTitleFrame = Frame(self)
    self.delayTitleFrame = Frame(self)
    self.selectionPolicyTitleFrame = Frame(self)
    self.rumorRuleTitleFrame = Frame(self)
    self.spreadTitleFrame = Frame(self)
    #========== Titles =========================
    self.displayTitleFrame.grid(row=1,column=0)
    self.edgeTitleFrame.grid(row=1,column=2)
    self.widthTitleFrame.grid(row=1,column=1)
    self.delayTitleFrame.grid(row=1,column=3)
    self.selectionPolicyTitleFrame.grid(row=1,column=4)
    self.rumorRuleTitleFrame.grid(row=1,column=5)
    self.spreadTitleFrame.grid(row=1,column=6)
    #=========== Functions ======================
    self.displayFrame.grid(row=2,column=0,rowspan=4)
    self.edgeFrame.grid(row=2,column=2,rowspan=4)
    self.widthFrame.grid(row=2,column=1,rowspan=4)
    self.delayFrame.grid(row=2,column=3,rowspan=4)
    self.selectionPolicyFrame.grid(row=2,column=4,rowspan=2)
    self.rumorRuleFrame.grid(row=2,column=5,rowspan=4)
    self.spreadFrame.grid(row=2,column=6,rowspan=2)
    self.buttonFrame.grid(row=1,column=7,rowspan=4)
    #============= Others ==========================
    self.info = LabelFrame(self,text="Node information")
    self.info.grid(row=0,column=7,sticky="NE")

  #====================
  def structures(self):
  #====================
    """
    Initialisation des structures
    """
    self.listUsedName = []          # Liste des noms utilisé
    self.allNode = []               # Liste des noeuds dans le réseau
    self.oldUsers = []              # Old users
    self.circulairDisplay = True    # Booléen True si le display est Circulaire
    self.selectObject = None        # Objet selectionné lors du Drag-and-Drop
    self.rollOverNode = None        # Noeud survolé
    self.activeThread = False
    self.startedPropagation = False
    self.activeMotion = False
    self.activeCluedo = False

#=========== Events ===========
  def events(self):
    """
    Evenement modification du Scale ( taille )
    """
    self.widthScale.bind("<ButtonRelease-"+self.LEFTCLICK+">",self.modifyWidth)

#=============================== Interface principale ===================================================
#--------------------------------------------------------------------------------------------------------
  def mainWidgets(self):
    """
    Regroupe tout mes widgets pour les placer dans la fenetre principale
    """
    self.addButton()
    self.propagateButton()
    self.runButton()
    self.resetButton()
    self.defaultButton()
    self.statisticsButton()
    self.nodeWidth()
    self.nodeEdge()
    self.checkDisplay()
    self.delay()
    self.selectionPolicy()
    self.rumorRule()
    self.probaModif()
    self.spread()
    self.information()
    self.menuOption()
    self.rightClickMenu()
    self.sendEveryoneWidget()
#===== Node informations =====
  def information(self):
    """
    A droite du canvas, les informations sur l'étape, la personne cliqué et
    le nombre d'étape totale.
    """
    Label(self.info,text="Name :",font=("Arial",10,"bold","underline")).pack()
    self.chosenNode = Label(self.info,text=self.baseInfo)
    self.chosenNode.pack()
    Label(self.info,text="Rumor :",font=("Arial",10,"bold","underline")).pack()
    self.chosenNodeRumor = Label(self.info,text=self.baseInfo)
    self.chosenNodeRumor.pack()
    Label(self.info,text="Step :",font=("Arial",10,"bold","underline")).pack()
    self.stepNumber = IntVar()
    self.stepNumber.set(0)
    Label(self.info,textvariable=self.stepNumber).pack()

#==== Buttons ====
  def addButton(self):
    Button(self.buttonFrame,text="New node",command=self.addUser,borderwidth=3).grid(sticky="WE")
  def propagateButton(self):
    Button(self.buttonFrame,text="Propagate",borderwidth=3,command=self.propagate1Step).grid(sticky="WE")
  def runButton(self):
    Button(self.buttonFrame,text="Run",command=self.run,borderwidth=3).grid(sticky="WE")
  def resetButton(self):
    Button(self.buttonFrame,text="Reset steps",borderwidth=3,command=self.resetSteps).grid(sticky="WE")
  def defaultButton(self):
    Button(self.buttonFrame,text="Set default",borderwidth=3,command=self.setDefault).grid(sticky="WE")
  def statisticsButton(self):
    Button(self.buttonFrame,text="Statistics",borderwidth=3,command=self.statistics).grid(sticky="WE")
#=== Display/Layout === 
  def checkDisplayTitle(self):
    Label(self.displayTitleFrame,text="Display",font=("Arial",13,"bold"),fg="#000000").grid(sticky="WE")
  def checkDisplay(self):
    self.checkDisplayTitle()
    self.varDisplay = IntVar()
    self.choice0 = Radiobutton(self.displayFrame,text="Circular",variable=self.varDisplay,value=0,command=self.displayModif)
    self.choice1 = Radiobutton(self.displayFrame,text="Random",variable=self.varDisplay,value=1,command=self.displayModif)
    self.choice0.pack()
    self.choice1.pack()
#=== node Width ===
  def nodeWidthTitle(self):
    Label(self.widthTitleFrame,text=" Node width",font=("Arial",13,"bold"),fg="#000000").grid(sticky="WE")
  def nodeWidth(self):
    self.nodeWidthTitle()
    self.valueWidth = DoubleVar()
    self.valueWidth.set(20)
    self.saveWidth = 20
    self.widthScale = Scale(self.widthFrame, from_=1,to=50,variable=self.valueWidth)
    self.widthScale.pack()
#=== node Edge ===
  def nodeEdgeTitle(self):
    Label(self.edgeTitleFrame,text=" Node edge",font=("Arial",13,"bold"),fg="#000000").grid(sticky="WE")
  def nodeEdge(self):
    self.nodeEdgeTitle()
    self.valueEdge = DoubleVar()
    self.valueEdge.set(2)
    self.edgeScale = Scale(self.edgeFrame,from_=1,to=10, variable=self.valueEdge)
    self.edgeScale.pack()
#=== Delay ===
  def delayTitle(self):
    Label(self.delayTitleFrame,text=" Delay",font=("Arial",13,"bold"),fg="#000000").grid(sticky="WE")
  def delay(self):
    self.delayTitle()
    self.valueDelay = DoubleVar()
    self.valueDelay.set(0.5)
    delay = Scale(self.delayFrame,from_=0.0,to=3.0,resolution=0.1,variable=self.valueDelay)
    delay.pack()
#=== Selection policy ===
  def selectionPolicyTitle(self):
    Label(self.selectionPolicyTitleFrame,text=" Selection policy",font=("Arial",13,"bold"),fg="#000000").grid(sticky="WE")
  def selectionPolicy(self):
    self.selectionPolicyTitle()
    self.listPolicy = Listbox(self.selectionPolicyFrame,exportselection=0,width=15,height=2,borderwidth=3)
    self.listPolicy.insert("0","Random")
    self.listPolicy.selection_set("0")
    self.listPolicy.activate("0")
    self.listPolicy.pack()
#=== Rumor Rule ===
  def rumorRuleTitle(self):
    Label(self.rumorRuleTitleFrame,text=" Rumor rule",font=("Arial",13,"bold"),fg="#000000").grid(sticky="WE")
  def rumorRule(self):
    self.rumorRuleTitle()
    self.listModification = Listbox(self.rumorRuleFrame,exportselection=0,width=15,height=3,borderwidth=3)
    self.listModification.insert("0","None")
    self.listModification.insert("1","Incremental")
    self.listModification.insert("2","Bitflip")
    self.listModification.selection_set("0")
    self.listModification.activate("0")
    self.listModification.pack()
  def probaModif(self):
    self.valueProba = DoubleVar()
    self.valueProba.set(0.5)
    proba = Scale(self.rumorRuleFrame,from_=0.0,to=1.0,resolution=0.1,orient=HORIZONTAL,variable=self.valueProba)
    proba.pack()
#=== Spread Rule ===
  def spreadTitle(self):
    Label(self.spreadTitleFrame,text=" Spread rule",font=("Arial",13,"bold"),fg="#000000").grid(sticky="WE")
  def spread(self):
    self.spreadTitle()
    self.listSpread = Listbox(self.spreadFrame,exportselection=0,width=15,height=3,borderwidth=3)
    self.listSpread.insert("0","Stable")
    self.listSpread.insert("1","Rewrite")
    self.listSpread.insert("2","Mixture")
    self.listSpread.selection_set("0")
    self.listSpread.activate("0")
    self.listSpread.pack()
    
#--------------------------------------------------------------------------------------------------------
#========================================================================================================

#============================  New node interface =====================================
  def gridTitle(self):
    Label(self.add,text="Already used names",font=("Arial",10,"bold"),fg="#000000").grid(row=0,column=0,columnspan=3)
  def newName(self):
    self.gridTitle()
    self.sendButton()
    self.nameList()
    self.entryLabel()
    self.entryVariable = StringVar()
    self.entry = Entry(self.add,textvariable = self.entryVariable,fg="#000000",borderwidth=3)
    self.entry.focus_set()
    self.entry.selection_range(0,END)
    self.entry.grid(row=2,column=1,sticky="EW")
  def entryLabel(self):
    Label(self.add,text="New node name :",font=("Arial",10,"bold"),fg="#000000").grid(row=2,column=0,sticky="W")
  def sendButton(self):
    Button(self.add,text="Send",command=self.validateName).grid(row=2,column=2)

  def addUser(self):
    """
    Fenêtre secondaire lors du clique sur le bouton new node
    """
    if not self.isStartedPropagation():
      try:
        self.add.lift()
      except:
        self.add = Toplevel()
        self.add.protocol("WM_DELETE_WINDOW",self.removeLastNode)
        self.add.title("Add")
        self.add.resizable(False,False)    
        self.add.grid()
        self.newName()
        #Premier moyen de lancer , press Enter.
        self.entry.bind("<Return>", self.validateName)
        #Creation d'un oval pour montrer la position qu'aura le nouveau noeud.
        self.lastAddNode = Person("New User",self.valueWidth.get())
        self.lastAddNode.dash = (10,10)
        self.lastAddNode.outline = NetworkFrame.NEWUSER
        self.allNode.append(self.lastAddNode)
        self.networkFrame.doRandomList(self)
        self.networkFrame.delete(ALL)
        self.addNodesOnCanvas()

  def removeLastNode(self):
    """
    Fermeture de la fenetre Add node
    """
    #Il faudra supprimer le noeud ajouté en pointillé pour montrer
    #la position qu'aurait pris le noeud s'il était créé
    self.networkFrame.delete(self.allNode[-1].oval)
    del self.allNode[-1]
    self.networkFrame.doRandomList(self)
    self.networkFrame.delete(ALL)
    self.addNodesOnCanvas()
    self.add.destroy()

  def nameList(self):
    """
    Liste avec scroll dans la fenetre secondaire New node
    Ne permet pas à l'utilisateur d'utiliser deux fois le même nom
    """
    #A l'ouverture, on met à jour la listBox.
    nameScroll = Scrollbar(self.add)
    nameScroll.grid(column=1,row=1,sticky="ENS")
    listNames = Listbox(self.add,yscrollcommand=nameScroll.set,borderwidth=5)
    listNames.grid(column=0,row=1,columnspan=3)
    nameScroll.config(command=listNames.yview)
    for elem in self.listUsedName:
      listNames.insert(END,elem)

  def validateName(self,event=0):
    """
    Vérifie si le nom est correcte
    Aucune convention si ce n'est qu'un noeud ne peut être utilisé
    qu'une fois
    """
    try:
      self.statisticNamesWindow.destroy()
    except:
      pass
    finally:
      name = self.entry.get()
      if len(name) == 0:
        showerror("Error","Atleast 1 character")
      elif name.upper() in self.listUsedName:
        showerror("Error","You can't use the same name twice !")
      else:
        self.allNode[-1].name = name.upper()
        self.allNode[-1].dash = None
        self.allNode[-1].outline = Person.BLACK
        self.listUsedName.append(name.upper())
        self.networkFrame.delete(ALL)
        self.addNodesOnCanvas()
        self.add.destroy()
#=================================== Propagate 1 step ==============================================
  def propagate1Step(self):
    """
    Propage la rumeur un tour
    """
    if not self.isActiveThread() and len(self.allNode) > 0:
      self.propagateTheRumor()
      self.stepNumber.set(self.stepNumber.get() + 1)
      self.networkFrame.delete(ALL)
      self.addNodesOnCanvas()
      self.startedPropagation = True

  def propagateTheRumor(self):
    """
    Modifie les rumors et propage par rapport aux options données
    par l'utilisateur
    """
    self.modifRule = self.listModification.get(ACTIVE).lower()
    self.spreadRule = self.listSpread.get(ACTIVE).lower()
    self.chosenProba = self.valueProba.get()
    #Pour mettre le réseau à jour à la fin de la simulation,
    #il faut deux listes supplémentaires
    self.listChosenFriends = []
    self.rumors = []
    self.labelInfo = ""
    self.modifyTheRumors()
    for i in range(len(self.listChosenFriends)):
      update = self.updateFunction()
      chosenOneRumor = int(self.listChosenFriends[i].rumor[1:],16)
      baseRumor = int(self.rumors[i][1:],16)
      newRumor = update(baseRumor,chosenOneRumor)
      newRumor = "#"+self.intToHexa(newRumor)
      if newRumor != self.listChosenFriends[i].rumor:
        self.listChosenFriends[i].oldRumors.append(self.listChosenFriends[i].rumor[1:])
      self.listChosenFriends[i].rumor = newRumor.upper()
      information = "{} learned {}".format\
      (self.listChosenFriends[i].name,newRumor[1:])
    for person in self.allNode:
      if person.knowsRumor():
        rumor = int(person.rumor[1:],16)
        self.addCluedoRumor(person)
                
  def modifFunction(self):
    """
    Dictionnaire clé/valeur dans le fichier rumorFunctions
    renvoie la fonction de modification de rumor 
    """
    return rF.modificationDict[self.modifRule]

  def updateFunction(self):
    """
    Dictionnaire clé/valeur dans le fichier rumorFunctions
    renvoie la fonction d'update
    """
    return rF.updateDict[self.spreadRule]

  def modifyTheRumors(self):
    """
    Mets à jour le réseau et chaque personne avec les nouvelles 
    rumeurs
    """
    for person in self.allNode:
        randProbability = random()
        # Repete la rumeur à tous ces amis
        if not bool(self.tellEvery.get()):
          if person.knowsRumor() and len(person.friends) > 0:
            chosenFriend = person.friends[randint(0,len(person.friends)-1)]
            self.listChosenFriends.append(chosenFriend)
            rumorToLearn = person.rumor[1:]
            if self.chosenProba >= randProbability:
              modify = self.modifFunction()
              rumorToLearn = self.intToHexa(modify(int(rumorToLearn,16))).upper()
              self.rumors.append(("#"+rumorToLearn))
            else:
              rumorToLearn = rumorToLearn.upper()
              self.rumors.append(("#"+rumorToLearn))
        else:
            potentialRumors = []
            for friend in self.allNode:
              if person != friend and friend.knowsRumor() and person in friend.friends:
                rumorToLearn = friend.rumor[1:]
                if self.chosenProba >= randProbability:
                  modify = self.modifFunction()
                  rumorToLearn = self.intToHexa(modify(int(rumorToLearn,16))).upper()
                if rumorToLearn != 0:
                  potentialRumors.append(rumorToLearn.upper())
            if len(potentialRumors)>0:
              mostCommonRumor = {}
              for rumor in potentialRumors:
                if rumor in mostCommonRumor:
                  mostCommonRumor[rumor] += 1
                else:
                  mostCommonRumor[rumor] = 1
              values = list(mostCommonRumor.values())
              keys = list(mostCommonRumor.keys())
              keyMax = keys[values.index(max(values))]
              flag = True
              for i in range(len(values)):
                if keys[i] != keyMax and max(values) == values[i]:
                  flag=False
              if flag:
                self.rumors.append("#"+keyMax)
              else:
                chosenRumor = randint(0,len(potentialRumors)-1)
                self.rumors.append("#"+potentialRumors[chosenRumor])
              self.listChosenFriends.append(person)

#================================ Run interface ====================================
  def titleEntry(self):
    Label(self.steps,text="How many steps ?").grid(row=0,column=0)
  def runSteps(self):
    Button(self.steps,text="Go",command=self.propagateSteps).grid(row=0,column=2)

  def run(self):
    """
    Fenêtre secondaire en cliquant sur le bouton Run
    Permets de simuler plusieurs tours avec un certain délai
    modifiable à tout moment
    """
    if not self.isActiveThread():
      try:
        self.steps.lift()
      except:
        self.steps = Toplevel()
        self.steps.title("Run steps")
        self.steps.resizable(False,False)
        self.titleEntry()
        self.runSteps()
        self.numberOfSteps = IntVar()
        self.stepsEntry = Entry(self.steps,textvariable = self.numberOfSteps,borderwidth=3)
        self.stepsEntry.focus_set()
        self.stepsEntry.selection_range(0,END)
        self.stepsEntry.bind("<Return>", self.propagateSteps)
        self.stepsEntry.grid(row=0,column=1)

  def propagateSteps(self,event=0):
    """
    Vérifie la valeur entrée dans Run
    """
    try:
      self.statisticNamesWindow.destroy()
    except:
      pass
    finally:
      maxSteps = 200    # Pour ne pas tourner trop longtemps, une valeur max de tours
      positive = 0
      try:
        steps = self.numberOfSteps.get()
      except:
        showerror("Error","An integer please")
      else:
        if steps <= maxSteps and steps >= positive:
          thread = PropagateThread(self)
          thread.start()
        else:
          showerror("Error","Run steps from 0 to 200")

#============================= Reset steps ====================================
  def resetSteps(self):
    """
    Mets le tour à 0, pour permettre la modification du réseau
    """
    if not self.isActiveThread():
      self.stepNumber.set(0)
      self.startedPropagation = False

#============================= Set Default ===================================
  def setDefault(self):
    """
    Bouton supplémentaire permettant de mettre les parametres par défaut
    """
    if not self.isActiveThread():
      self.valueWidth.set(20)
      self.valueEdge.set(2)
      self.valueDelay.set(0.5)
      self.valueProba.set(0.5)
      self.listModification.selection_clear("0","2")
      self.listSpread.selection_clear("0","2")
      self.listModification.selection_set("0")
      self.listSpread.selection_set("0")
      self.listModification.activate("0")
      self.listSpread.activate("0")
      self.chosenNode.config(text=self.baseInfo)
      self.chosenNodeRumor.config(text=self.baseInfo)
      self.modifyWidth()
    
#=============================== Start ===================================
  def startCanvas(self):
    """
    Initialise le canvas et ses evenements
    """
    self.networkFrame = NetworkFrame(self,self.circulairDisplay)
    self.networkFrame.grid(row=0,column=0,columnspan=6)
    self.networkFrame.bind("<Button-"+self.LEFTCLICK+">",self.personClick)    
    self.networkFrame.bind("<Button-"+self.RIGHTCLICK+">",self.rightClick)
    self.networkFrame.bind("<Button"+self.LEFTCLICK+"-Motion>",self.nodeMotion)
    self.networkFrame.bind("<Button"+self.LEFTCLICK+"-ButtonRelease>",self.newLink)

  def addNodesOnCanvas(self):
    """
    Ajoute les noeuds sur le réseau avec le display selectionné
    """
    if len(self.allNode) > 0:
      self.networkFrame.addDisplay(self)

  def addNamesOnCanvas(self):
    for person in self.allNode:
      x,y = person.middle[0],person.middle[1]
      if y > (NetworkFrame.CANVASHEIGHT)/2:
        self.networkFrame.create_text(x,y+person.width+10,text=person.name,font=("Arial",10,"bold"))
      else:
        self.networkFrame.create_text(x,y-person.width-10,text=person.name,font=("Arial",10,"bold"))

#========================= Size Modifications ============================
  #Modification de la taille des noeuds par refresh.
  def modifyWidth(self,event=0):
    """
    Modifie la taille des noeuds avec une formule pour ne pas avoir 
    une différence trop importante entre la taille min et max
    """
    if not self.isActiveThread():
      for person in self.allNode:
        person.width = 15 + (self.valueWidth.get())/10
      self.networkFrame.delete(ALL)        
      self.addNodesOnCanvas()
      self.saveWidth = self.valueWidth.get()
    else:
      self.valueWidth.set(self.saveWidth)

#========================== Roll over a node ==========================
  #Recherche du noeud cliqué.
  def verifyClickPosition(self,x,y):
    """
    Cherche le noeud le plus proche de l'endroit cliqué ou survolé
    """
    users = len(self.allNode)
    i = 0
    flag = False
    while i<users and not flag:
      if self.allNode[i].x0<=x<=self.allNode[i].x1 and \
      self.allNode[i].y0<=y<=self.allNode[i].y1:
        self.rollOverNode = self.allNode[i]
        flag = True
      else:
        i+=1
    return flag

  def personClick(self,event):
    """
    Clique gauche sur un noeud pour la selectionner
    """
    #Avant de maintenir, reperer le noeud cliqué.
    if not self.isActiveThread() and self.verifyClickPosition(event.x,event.y):
        self.x,self.y = event.x , event.y
        self.motionNode = self.rollOverNode
        self.selectObject = self.motionNode.oval
        self.activeMotion = True

  def nodeMotion(self,event):
    """
    Motion du noeud selectionné
    """
    #Maintient du clique gauche sur une personne pour créer un lien
    #d'amitié
    if not self.isStartedPropagation() and self.selectObject:
      x1, y1 = event.x, event.y
      moveX , moveY = x1 - self.x , y1 - self.y
      self.networkFrame.itemconfig(self.selectObject, width=5,outline=self.NODELIFT)
      self.networkFrame.move(self.selectObject, moveX, moveY)
      self.networkFrame.lift(self.selectObject)
      self.x,self.y = x1, y1

  def newLink(self,event):
    """
    Lacher du clique, création d'un lien d'amitié si l'emplacement est correcte
    """
    if self.selectObject:
      self.selectObject = None
      if self.verifyClickPosition(self.x,self.y) and self.motionNode != self.rollOverNode:
        if self.rollOverNode not in self.motionNode.friends:
          self.motionNode.friends.append(self.rollOverNode)
      #Si le lieu où le clique est laché correspond au noeud d'une personne,
      #On affiche ces liens d'amitié
      if self.verifyClickPosition(event.x,event.y):
        self.networkFrame.delete(ALL)
        self.rollOverNodeLinks()
        self.addNodesOnCanvas()
        self.networkFrame.itemconfig(self.rollOverNode.oval,outline=NetworkFrame.NEWUSER)
        self.chosenNode.config(text=self.rollOverNode.name)
        if self.activeCluedo:
          self.chosenNodeRumor.config(text=self.rollOverNode.cluedoRumor)
        else:
          self.chosenNodeRumor.config(text=str(int(self.rollOverNode.rumor[1:],16)))
      else:
        self.rollOverNode = None
        self.chosenNode.config(text=self.baseInfo)
        self.chosenNodeRumor.config(text=self.baseInfo)
        self.networkFrame.delete(ALL)          
        self.rollOverNodeLinks()
        self.addNodesOnCanvas()
    try:
      self.statisticNamesWindow.destroy()
    except:
      pass
    finally:
      self.activeMotion = False

  def enterItem(self,event):
    """
    Survole un noeud
    """
    x,y = event.x,event.y
    if not self.isActiveThread() and not self.activeMotion and \
    not self.notIsNone(self.rollOverNode) and self.verifyClickPosition(x,y):
      self.networkFrame.delete(ALL)
      self.rollOverNodeLinks()
      self.addNodesOnCanvas()
      self.networkFrame.itemconfig(self.rollOverNode.oval,outline = NetworkFrame.NEWUSER)
      self.networkFrame.lift(self.rollOverNode.oval)
      self.chosenNode.config(text=self.rollOverNode.name)
      if self.activeCluedo:
        self.chosenNodeRumor.config(text=self.rollOverNode.cluedoRumor)
      else:
        if self.rollOverNode.knowsRumor():
          self.chosenNodeRumor.config(text=str(int(self.rollOverNode.rumor[1:],16)))
        else:
          self.chosenNodeRumor.config(text="Doesn't know\n the rumor")
    
  def leaveItem(self,event):
    """
    Quitter un noeud
    """
    x,y = event.x,event.y
    if not self.isActiveThread() and not self.activeMotion and self.notIsNone(self.rollOverNode):
      self.rollOverNode.outline = Person.BLACK
      self.rollOverNode = None
      self.networkFrame.delete(ALL)
      self.addNodesOnCanvas()
      self.chosenNode.config(text=self.baseInfo)
      self.chosenNodeRumor.config(text=self.baseInfo)

  def rollOverNodeLinks(self):
    """
    Affichage des liens d'amitié de la personne survolée sur le réseau
    """
    if self.notIsNone(self.rollOverNode):
      self.rollOverNode.friendsLink(self)

#=============================== Change display ==========================================
  def displayModif(self):
    """
    Modifie le display par rapport au layout selectionné 
    si celui-ci n'était pas déjà selectionné
    """
    if self.isActiveThread():
      showerror("Error","You can't modify the display during propagation")
      if self.varDisplay.get() == 0:
        self.choice1.select()
      else:
        self.choice0.select()
    else:
      flag = False
      #== 0 et == 1 étant les valeurs des layouts, on pourrait en avoir plus,
      #donc on ne peut utiliser deux booléens
      if self.varDisplay.get() == 0 and not self.circulairDisplay:
        self.circulairDisplay = True
        flag = True
      elif self.varDisplay.get() == 1 and self.circulairDisplay:
        self.circulairDisplay = False
        flag = True
      if flag:
        self.chosenNode.config(text=self.baseInfo)
        self.chosenNodeRumor.config(text=self.baseInfo)
        if len(self.allNode)>0:
          self.networkFrame.delete(ALL)
          self.addNodesOnCanvas()

#=============================== Modif Color Right Click ============================        
  def rightClickMenu(self):
    """
    Différents options du clique droit sur un noeud
    """
    self.rightMenu = Menu(self,tearoff=0)
    self.rightMenu.add_command(label="Modify rumor",command=self.popModifyRumor)
    self.rightMenu.add_command(label="Modify friendship",command=self.popModifyFriendship)

  def rightClick(self,event):
    if self.verifyClickPosition(event.x,event.y):
      self.toModif = self.rollOverNode
      if not self.isStartedPropagation():
        self.rightMenu.post(event.x_root,event.y_root)

  def popModifyRumor(self):
    """
    Modification de la couleur ( rumeur ) d'une personne 
    """
    if not self.activeCluedo:
      self.color = askcolor(title=self.toModif.name)
      if self.notIsNone(self.color[0]):
        self.colorModification()
    else:
      self.modifyCluedoRumorWindow = Toplevel()
      self.modifyCluedoRumorWindow.resizable(False,False)
      suspectScroll = Scrollbar(self.modifyCluedoRumorWindow)
      suspectScroll.grid(row=0,column=1,sticky="NS")
      armeScroll = Scrollbar(self.modifyCluedoRumorWindow)
      armeScroll.grid(row=0,column=3,sticky="NS")
      lieuScroll = Scrollbar(self.modifyCluedoRumorWindow)
      lieuScroll.grid(row=0,column=5,sticky="NS")
      self.listboxSuspect = Listbox(self.modifyCluedoRumorWindow,exportselection=0,yscrollcommand=suspectScroll.set,width=30,borderwidth=3)
      self.listboxArme = Listbox(self.modifyCluedoRumorWindow,exportselection=0,yscrollcommand=armeScroll.set,width=30,borderwidth=3)
      self.listboxLieu = Listbox(self.modifyCluedoRumorWindow,exportselection=0,yscrollcommand=lieuScroll.set,width=30,borderwidth=3)
      suspectScroll.config(command=self.listboxSuspect.yview)
      armeScroll.config(command=self.listboxArme.yview)
      lieuScroll.config(command=self.listboxLieu.yview)
      for suspect in self.cluedoSuspect:
        self.listboxSuspect.insert(END,suspect)
      for arme in self.cluedoArme:
        self.listboxArme.insert(END,arme)
      for lieu in self.cluedoLieu:
        self.listboxLieu.insert(END,lieu)
      self.listboxSuspect.grid(row=0,column=0)
      self.listboxArme.grid(row=0,column=2)
      self.listboxLieu.grid(row=0,column=4)
      Button(self.modifyCluedoRumorWindow,text="OK",command=self.cluedoModification).grid(row=0,column=6)

  def cluedoModification(self):
    self.toModif.cluedoSuspect = self.listboxSuspect.get(ACTIVE)
    self.toModif.cluedoArme = self.listboxArme.get(ACTIVE)
    self.toModif.cluedoLieu = self.listboxLieu.get(ACTIVE)
    self.toModif.cluedoRumor = "{} \na tué le docteur Lenoir\n avec {}\n {}".format(self.toModif.cluedoSuspect,self.toModif.cluedoArme,self.toModif.cluedoLieu)
    self.modifyCluedoRumorWindow.destroy()
    showinfo("New cluedo rumor","{}'s new rumor is\n {}".format(self.toModif.name,self.toModif.cluedoRumor))

  #Fenetre secondaire avec tableau pour suppresion des liens d'amitié
  def modifyFriendshipWindow(self):
    """
    Fenetre secondaire lors de la suppression de lien d'amitié
    """
    self.toModifFriendship = self.toModif
    self.friendship = Toplevel()
    self.friendship.title(self.toModifFriendship.name)
    self.friendship.resizable(False,False)
    self.friendship.grid()
    Label(self.friendship,text="Friendship to delete").pack()
    self.listFriends = Listbox(self.friendship)
    self.listFriends.selection_set("0")
    self.listFriends.activate("0")
    self.listFriends.pack()
    Button(self.friendship,text="Delete",command=self.removeFriendship).pack()
    for friend in self.toModifFriendship.friends:
      self.listFriends.insert(END,friend.name)
  
  def popModifyFriendship(self):
    """
    Suppression de la fenetre de modification si elle était ouverte
    et ouverture de la nouvelle
    """
    if not self.isStartedPropagation():
      try:
        self.friendship.destroy()
        self.modifyFriendshipWindow()
      except:
        self.modifyFriendshipWindow()
  
  def colorModification(self):
    """
    Modifie la couleur d'une personne sur le canvas
    """
    try:
      self.statisticNamesWindow.destroy()
    except:
      pass
    finally:
      newRumor = self.color[1]
      self.networkFrame.itemconfig(self.toModif.oval,fill = newRumor)
      self.toModif.oldRumors.append(self.toModif.rumor[1:])
      self.toModif.rumor = newRumor.upper()
      if int(self.toModif.rumor[1:],16) != 0:
        self.addCluedoRumor(self.toModif)
    
#========================== Barre d'options  ==============================
  def menuOption(self):
    """
    Options du fileMenu , permet de charger et sauvegarder un réseau.
    Seulement les noeuds et les liens d'amitié sont sauvegardé et chargé
    Permet également de réinitialiser le réseau
    """
    self.menuBar = Menu(self)
    fileMenu = Menu(self.menuBar,tearoff=0)
    fileMenu.add_command(label="New",command=self.newNetwork)
    fileMenu.add_separator()
    fileMenu.add_command(label="Save",command=self.saveNetwork)
    fileMenu.add_command(label="Load",command=self.loadNetwork)
    fileMenu.add_separator()
    fileMenu.add_command(label="Quit",command=self.quit)
    customMenu = Menu(self.menuBar,tearoff=0)
    customMenu.add_command(label="Custom Network",command=self.customNumberUser)
    self.menuBar.add_cascade(label="File",menu=fileMenu)
    self.menuBar.add_cascade(label="Network",menu=customMenu)
    cluedoMenu = Menu(self.menuBar,tearoff=0)
    if self.activeCluedo:
      cluedoMenu.add_command(label="Disable Cluedo",command=self.ableOrDisableCluedo)
    else:
      cluedoMenu.add_command(label="Able Cluedo",command=self.ableOrDisableCluedo)
    cluedoMenu.add_command(label="Modify Cluedo",command=self.modifCluedo)
    self.menuBar.add_cascade(label="Cluedo",menu=cluedoMenu)
    helpMenu = Menu(self.menuBar,tearoff=0)
    helpMenu.add_command(label="How to use",command=self.helpMessage)
    helpMenu.add_command(label="About ...",command=self.aboutMessage)
    self.menuBar.add_cascade(label="Help",menu=helpMenu)

    self.parent.config(menu=self.menuBar)

  def saveNetwork(self):
    """
    Sauvegarde un fichier .txt du réseau actuel
    """
    if not self.isActiveThread():
      pressCancel = ""
      fileToWrite = filedialog.asksaveasfilename(title="Save your file",filetypes=[("Txt files","*.txt")])
      if fileToWrite != pressCancel:
        fileWriting = open(fileToWrite,"w")
        fileWriting.write(str(self.activeCluedo))
        fileWriting.write("-")
        fileWriting.write(self.listModification.get(ACTIVE).lower())
        fileWriting.write("-")
        fileWriting.write(self.listSpread.get(ACTIVE).lower())
        fileWriting.write("-")
        fileWriting.write(str(float(self.valueProba.get())))
        fileWriting.write("-")
        fileWriting.write(str(self.tellEvery.get()))
        fileWriting.write("-")
        fileWriting.write(str(self.stepNumber.get()))
        fileWriting.write("\n")
        for person in self.allNode:
          fileWriting.write(person.name+ ":")
          for i in range(len(person.friends)):
            if i != 0:
              fileWriting.write(",")
            fileWriting.write(person.friends[i].name)
          fileWriting.write(";")
          fileWriting.write(str(int(person.rumor[1:],16)))
          fileWriting.write("\n")
        fileWriting.close()

  def loadNetwork(self):
    """
    Chargement d'un réseau via un fichier .txt
    """
    try:
      self.statisticNamesWindow.destroy()
    except:
      pass
    finally:
      if not self.isActiveThread():
        pressCancel = ""
        fileToOpen = filedialog.askopenfilename(title="Choose your file",filetypes=[("Txt files","*.txt")])
        if fileToOpen != pressCancel:
          fileReading = open(fileToOpen)
          network = fileReading.readlines()
          details = network[0]
          network = network[1:]
          fileReading.close()
          self.newNetwork()
          friendPerNode = []
        try:
          splitDetails = "-"
          splitPerson = ":"
          splitRumor = ";"
          splitFriends = ","
          listModif = ["none","incremental","bitflip"]
          listSpread = ["stable","rewrite","mixture"]
          details = details.split(splitDetails)
          if details[0] == "False":
            self.activeCluedo = True
            self.sendEveryone.select()
          else:
            self.activeCluedo = False
            self.sendEveryone.deselect()
          self.ableOrDisableCluedo()
          self.listModification.selection_clear("0",END)
          self.listModification.selection_set(str(listModif.index(details[1])))
          self.listModification.activate(str(listModif.index(details[1])))
          self.listSpread.selection_clear("0",END)
          self.listSpread.selection_set(str(listSpread.index(details[2])))
          self.listSpread.activate(str(listSpread.index(details[2])))
          self.valueProba.set(details[3])
          if bool(int(details[4].strip())):
            self.sendEveryone.select()
          else:
            self.sendEveryone.deselect()
          self.stepNumber.set(int(details[5]))
          if int(details[5]) > 0:
            self.startedPropagation = True
            
          for elem in network:
            elem = elem.split(splitPerson)
            self.listUsedName.append(elem[0].strip().upper())
            self.allNode.append(Person(elem[0].strip().upper(),self.valueWidth.get()))
            if elem[1][0] != splitRumor:
              friendsAndRumor = elem[1].split(splitRumor)
              rumor = int(friendsAndRumor[1].strip())

              self.allNode[-1].rumor = "#"+str(self.intToHexa(rumor))
              if rumor != 0:
                self.addCluedoRumor(self.allNode[-1])
              friendPerNode.append(friendsAndRumor[0].strip())
            else:
              friends = ""
              rumor = int(elem[1][1:].strip())
              self.allNode[-1].rumor = "#"+str(self.intToHexa(rumor))
              if rumor != 0:
                self.addCluedoRumor(self.allNode[-1])
              friendPerNode.append(friends)
          self.networkFrame.delete(ALL)
          self.networkFrame.doRandomList(self)
          self.addNodesOnCanvas()
          users = len(self.allNode)
          for i in range(users):
            node = self.allNode[i]
            friendsOfNode = friendPerNode[i].split(splitFriends)
            for elem in friendsOfNode:
              if len(elem)>0:
                j=0
                found = False
                while not found:
                  if self.allNode[j].name == elem.strip().upper():
                    found = True
                  else:
                    j+=1
                node.friends.append(self.allNode[j])
        except:
          self.newNetwork()
          showerror("Error","The txt file is badly written")
  
  def newNetwork(self):
    """
    Réinitialise le réseau
    """
    try:
      self.statisticNamesWindow.destroy()
    except:
      pass
    finally:
      if not self.isActiveThread():
        self.startCanvas()
        self.listUsedName = []
        self.allNode = []
        self.oldUsers = []
        self.selectObject = None
        self.rollOverNode = None
        self.startedPropagation = False
        self.chosenNode.config(text=self.baseInfo)
        self.chosenNodeRumor.config(text=self.baseInfo)
        self.resetSteps()

#======================= Supplémentaires ====================================

  def isActiveThread(self):
    """
    Retourne un booléen True et affiche un message d'erreur si un RUN est actif
    Certaines options sont confisqués si celui-ci est actif
    """
    if self.activeThread:
      showerror("Error","The propagation is runing")
      self.activeMotion = False
    return self.activeThread

  def isStartedPropagation(self):
    """
    Retourne un booléen True et affiche un message d'erreur si la propagation a déjà commencé.
    Certaines options sont confisqués si celui-ci est actif
    """
    if self.startedPropagation:
      showerror("Error","The propagation already started")
      self.activeMotion = False
    return self.startedPropagation

  #Suppression des liens d'amitié entre 2 personnes.
  #Pour cette partie, maintenir la convention A ami avec B
  #signifie B ami avec A.
  def removeFriendship(self):
    """
    Supprime les liens d'amitié entre les deux personnes lors de la confirmation
    de suppression
    """
    try:
      self.statisticNamesWindow.destroy()
    except:
      pass
    finally:
      if len(self.toModifFriendship.friends)>0:
        activatePerson = self.listFriends.get(ACTIVE)
        showinfo("Remove relationship","{} is not friend with {} anymore"\
          .format(self.toModifFriendship.name,activatePerson))
        i=0
        while self.toModifFriendship.friends[i].name != activatePerson:
          i+=1
        if activatePerson not in self.toModifFriendship.oldFriends:
          self.toModifFriendship.oldFriends.append(activatePerson)
        del self.toModifFriendship.friends[i]
      else:
        showinfo("Info","The user has no friendship to delete")
      self.friendship.destroy()


  def removeNode(self,event):
    """
    Supprime un noeud du canvas et l'efface totalement du réseau
    """
    try:
      self.statisticNamesWindow.destroy()
    except:
      pass
    finally:
      if self.verifyClickPosition(event.x,event.y):
        self.oldUsers.append(self.rollOverNode.name)
        for person in self.allNode:
          if self.rollOverNode in person.friends:
            del person.friends[person.friends.index(self.rollOverNode)]
          elif self.rollOverNode.name in person.oldFriends:
            del person.oldFriends[person.oldFriends.index(self.rollOverNode.name)]
        del self.listUsedName[self.listUsedName.index(self.rollOverNode.name)]
        del self.allNode[self.allNode.index(self.rollOverNode)]
        self.startCanvas()
        if self.verifyClickPosition(event.x,event.y):
          self.rollOverNodeLinks()
          self.chosenNode.config(text=self.rollOverNode.name)
          if self.activeCluedo:
            self.chosenNodeRumor.config(text=self.rollOverNode.cluedoRumor)
          else:
            self.chosenNodeRumor.config(text=str(int(self.rollOverNode.rumor[1:],16)))
        else:
          self.chosenNode.config(text=self.baseInfo)
          self.chosenNodeRumor.config(text=self.baseInfo)
        self.networkFrame.doRandomList(self)
        self.addNodesOnCanvas()
    
  def helpMessage(self):
    showinfo("Help","Open help.txt in the same directory")

  def aboutMessage(self):
    showinfo("About","A rumor propagation simulator made by Yasin Arslan.") 

  def notIsNone(self,x):
    return x != None

  def intToHexa(self,x):
    return ("0x%0.6X" %x)[2:]
#================= Statistiques ======================
  def statistics(self):
    """
    Fenetre principale de statistiques
    """
    try:
      self.statisticWindow.destroy()
    except:
      pass
    finally:
      self.statisticWindow = Toplevel()
      self.statisticWindow.title("Stats")
      self.statisticWindow.resizable(False,False)
      if len(self.allNode)>0:
        minFriends,maxFriends,averageFriends = len(self.allNode[0].friends),len(self.allNode[0].friends),0
      else:
        minFriends,maxFriends,averageFriends = "/","/","/"
      knows = 0
      for person in self.allNode:
        if person.rumor != Person.BLACK:
          knows += 1
        if len(person.friends) > maxFriends:
          maxFriends = len(person.friends)
        if len(person.friends) < minFriends:
          minFriends = len(person.friends)
        averageFriends += len(person.friends)
      if len(self.allNode) > 0:
        averageFriends /= len(self.allNode)

      globalStatsFrame = LabelFrame(self.statisticWindow,text="Current step stats")
      globalStatsFrame.grid(row=0,column=0,sticky="EWNS")
      Label(globalStatsFrame,text="Current step : {}".format(self.stepNumber.get())).grid(sticky="EWNS")
      Label(globalStatsFrame,text="Total users in the network : {}".format(len(self.allNode))).grid(sticky="EWNS")
      Label(globalStatsFrame,text="Knows the rumor : {}".format(knows)).grid(sticky="EWNS")
      Label(globalStatsFrame,text="Doesn't know the rumor : {}".format(len(self.allNode)-knows)).grid(sticky="EWNS")
      Label(globalStatsFrame,text="Min friends :  {}".format(minFriends)).grid(sticky="EWNS")
      Label(globalStatsFrame,text="Max friends :  {}".format(maxFriends)).grid(sticky="EWNS")
      Label(globalStatsFrame,text="Average friends : {}".format(averageFriends)).grid(sticky="EWNS") 
  
      otherStatsFrame = LabelFrame(self.statisticWindow,text="Other stats")
      otherStatsFrame.grid(row=1,column=0,sticky="EWNS")
      
      Button(otherStatsFrame,text="All friendships",command=self.statisticFriendships).grid(row=0,column=0,sticky="EW")
      Button(otherStatsFrame,text="All rumors",command=self.statisticRumors).grid(row=0,column=1,sticky="EW")

  def statisticFriendships(self):
    """
    Fenetre des statistiques d'amitié
    """
    self.statisticWindow.destroy()
    try:
      self.statisticNamesWindow.lift()
    except:
      self.statisticNamesWindow = Toplevel()
      self.statisticNamesWindow.title("Friendships")
      self.statisticNamesWindow.resizable(False,False)
      nameScroll = Scrollbar(self.statisticNamesWindow)
      nameScroll.grid(column=1,row=0,sticky="ENS")
      self.statisticList = Listbox(self.statisticNamesWindow,yscrollcommand=nameScroll.set,borderwidth=5)
      self.statisticList.grid(column=0,row=0)
      nameScroll.config(command=self.statisticList.yview)
      for elem in self.listUsedName:
        self.statisticList.insert(END,elem)
      self.statisticList.bind("<<ListboxSelect>>",self.personFriends)

  def personFriends(self,event):
    """
    Statistiques des amis anciens et actuels personnelles
    """
    if len(self.allNode)>0:
      chosen = self.statisticList.curselection()
      chosen = self.statisticList.get(chosen)
      i = 0
      while self.listUsedName[i] != chosen:
        i+=1
      self.frameFriends = LabelFrame(self.statisticNamesWindow,text="Actual friends",\
        font=("Arial",10,"bold","underline"))
      self.frameOldFriends = LabelFrame(self.statisticNamesWindow,text="Old friends",\
        font=("Arial",10,"bold","underline"))
      self.frameFriends.grid(row=0,column=2,sticky="EWNS")
      self.frameOldFriends.grid(row=0,column=3,sticky="EWNS")
      for friend in self.allNode[i].friends:
        Label(self.frameFriends,text=friend.name).grid()
      for oldFriend in self.allNode[i].oldFriends:
        Label(self.frameOldFriends,text=oldFriend).grid()
      Label(self.frameFriends,text="").grid()
      Label(self.frameOldFriends,text="").grid()
      
  def statisticRumors(self):
    """
    Fenetre des statistiques de rumeur personnelle
    """
    self.statisticWindow.destroy()
    try:
      self.statisticRumorsWindow.lift()
    except:
      self.statisticRumorsWindow = Toplevel()
      self.statisticRumorsWindow.title("Rumors")
      self.statisticRumorsWindow.resizable(False,False)
      nameScroll = Scrollbar(self.statisticRumorsWindow)
      nameScroll.grid(column=1,row=0,sticky="ENS")
      self.rumorsList = Listbox(self.statisticRumorsWindow,yscrollcommand=nameScroll.set,borderwidth=5)
      self.rumorsList.grid(column=0,row=0)
      nameScroll.config(command=self.rumorsList.yview)
      for elem in self.listUsedName:
        self.rumorsList.insert(END,elem)
      self.rumorsList.bind("<<ListboxSelect>>",self.personRumors)
      
  def personRumors(self,event):
    """
    Statistiques des rumeurs personnelles
    """
    if len(self.allNode)>0:
      chosen = self.rumorsList.curselection()
      chosen = self.rumorsList.get(chosen)
      i = 0
      while self.listUsedName[i] != chosen:
        i+=1
      self.frameRumor = LabelFrame(self.statisticRumorsWindow,text="Actual Rumor")
      self.frameOldRumor = LabelFrame(self.statisticRumorsWindow,text="Old rumors")
      self.frameRumor.grid(row=0,column=3,sticky="EWNS")
      self.frameOldRumor.grid(row=0,column=4,sticky="EWNS")
      Label(self.frameRumor,text=self.allNode[i].rumor[1:]).grid()
      for elem in self.allNode[i].oldRumors:
        Label(self.frameOldRumor,text=elem).grid()
      Label(self.frameOldRumor,text="").grid()

#================= Custom Network ====================

  def customNumberUser(self):
    """
    Demande le nombre d'utilisation pour le nouveau réseau
    """
    try:
      self.customNumberWindow.lift()
    except:
      self.customNumberWindow = Toplevel()
      self.customNumberWindow.title("Custom network")
      Label(self.customNumberWindow,text="You can create a customized network").grid(row=0,column=0,columnspan=2,sticky="EWNS")
      Label(self.customNumberWindow,text="Number of users : ").grid(row=1,column=0)
      numberOfUsers = IntVar()
      self.usersEntry = Entry(self.customNumberWindow,textvariable = numberOfUsers,borderwidth=3)
      self.usersEntry.focus_set()
      self.usersEntry.selection_range(0,END)
      self.usersEntry.bind("<Return>", self.customNetwork)
      self.usersEntry.grid(row=1,column=1)
      Button(self.customNumberWindow,text="Create",command=self.customNetwork).grid(row=1,column=2)

  def customNetwork(self,event=0):
    """
    Création d'un réseau personnaliser par rapport aux réponses données à une suite
    de boite de dialogue
    """
    if not self.isActiveThread():
      self.newNetwork()
      flag = True
      minName = 1
      maxName = 8
      try:
        users = int(self.usersEntry.get())
      except:
        showerror("Error","An integer please")
      else:
        self.customNumberWindow.destroy()
        if askyesno("Network","Do you want a random Network ?"):
          for i in range(users):
            lenName = randint(minName,maxName)
            name = ""
            for j in range(lenName):
              name += chr(randint(ord("A"),ord("Z")))
            self.allNode.append(Person(name,self.valueWidth.get()))
            self.listUsedName.append(name.upper())
          #A peut être ami avec B sans que B ne soit ami avec A
          probaBeingFriend = 1    # 5 Chances sur 10 qu'il soit ami
          for k in range(users):
            for l in range(users):
              if k != l and randint(0,1)!=probaBeingFriend:
                self.allNode[k].friends.append(self.allNode[l])
        else:
          width = self.valueWidth.get()
          i = 0
          while flag and i < users:
            name = askstring("Create person","Enter a name ")
            if name == None:
              showinfo("Restart network","You restarted the network by pressing \"Cancel\"")
              self.newNetwork()
              flag = False
            else:
              while len(name)==0 or name.upper() in self.listUsedName:
                showerror("Error","You have to enter a name and you can't use the same name twice")
                name = askstring("Create person","Enter a name ")
              self.allNode.append(Person(name.upper(),width))
              self.listUsedName.append(name.upper())
              i+=1
          if flag:
            for person in self.allNode:
              for potentialFriend in self.allNode:
                if person != potentialFriend and askyesno("Friendship","is {} friend with {}".format(person.name,potentialFriend.name)):
                  person.friends.append(potentialFriend)                

        if flag and askyesno("Rumors","Do people know the rumor ?"):
          maxNumber = 16777215
          for person in self.allNode:
            rumor = randint(0,maxNumber)
            person.rumor = "#" + self.intToHexa(rumor)
            if rumor != 0:
              self.addCluedoRumor(person)
        self.networkFrame.doRandomList(self)
        self.addNodesOnCanvas()
        self.statistics()

#====================== Envoyer à tous ses amis =======================
  def sendEveryoneWidget(self):
    """
    Widget Checkbutton pour activer ou descativer l'envoi à tout ses amis
    """
    self.tellEvery = IntVar()
    self.sendEveryone = Checkbutton(self.spreadFrame,text="Send to all friends",variable = self.tellEvery,onvalue = 1,offvalue=0)
    self.sendEveryone.pack()

#===================== Cluedo ============================
  def ableOrDisableCluedo(self):
    """
    Activation ou déscativation du cluedo
    """
    save = float(self.valueProba.get())
    for elem in self.spreadFrame.winfo_children():
      elem.destroy()
    for elem in self.rumorRuleFrame.winfo_children():
      elem.destroy()
    self.listSpread = Listbox(self.spreadFrame,exportselection=0,width=15,height=3,borderwidth=3)
    self.listSpread.insert("0","Stable")
    self.listSpread.insert("1","Rewrite")

    self.listModification = Listbox(self.rumorRuleFrame,exportselection=0,width=15,height=3,borderwidth=3)
    self.listModification.insert("0","None")
    self.listModification.insert("1","Incremental")
    if self.activeCluedo:
      self.listSpread.insert("2","Mixture")
      self.listModification.insert("2","Bitflip")
      
    self.listSpread.selection_set("0")
    self.listSpread.activate("0")
    self.listSpread.pack()
    self.listModification.selection_set("0")
    self.listModification.activate("0")
    self.listModification.pack()
    self.probaModif()
    self.valueProba.set(save)
    self.sendEveryoneWidget()

    self.activeCluedo = not self.activeCluedo
    self.menuOption()
    

  def addCluedoRumor(self,person):
    """
    Ajoute la rumeur cluedo à un utilisateur
    """
    rumor = int(person.rumor[1:],16)
    person.cluedoSuspect = self.cluedoSuspect[rumor%len(self.cluedoSuspect)]
    person.cluedoArme = self.cluedoArme[rumor%len(self.cluedoArme)]
    person.cluedoLieu = self.cluedoLieu[rumor%len(self.cluedoLieu)]
    person.cluedoRumor = "{} \na tué le docteur Lenoir\n avec {}\n {}".format(person.cluedoSuspect,person.cluedoArme,person.cluedoLieu)
    
  def modifCluedo(self):
    """
    Fenetre à trois listbox pour la modification du cluedo
    """
    try:
      self.modifCluedoWindow.lift()
    except:
      self.modifCluedoWindow = Toplevel()
      self.modifCluedoWindow.title("Modify cluedo")
      self.modifCluedoWindow.resizable(False,False)
      suspectScroll = Scrollbar(self.modifCluedoWindow)
      suspectScroll.grid(row=0,column=1,sticky="NS")
      armeScroll = Scrollbar(self.modifCluedoWindow)
      armeScroll.grid(row=0,column=3,sticky="NS")
      lieuScroll = Scrollbar(self.modifCluedoWindow)
      lieuScroll.grid(row=0,column=5,sticky="NS")
      self.listboxSuspect = Listbox(self.modifCluedoWindow,exportselection=3,yscrollcommand=suspectScroll.set,width=30,borderwidth=3)
      self.listboxArme = Listbox(self.modifCluedoWindow,exportselection=1,yscrollcommand=armeScroll.set,width=30,borderwidth=3)
      self.listboxLieu = Listbox(self.modifCluedoWindow,exportselection=2,yscrollcommand=lieuScroll.set,width=30,borderwidth=3)
      suspectScroll.config(command=self.listboxSuspect.yview)
      armeScroll.config(command=self.listboxArme.yview)
      lieuScroll.config(command=self.listboxLieu.yview)
      for suspect in self.cluedoSuspect:
        self.listboxSuspect.insert(END,suspect)
      for arme in self.cluedoArme:
        self.listboxArme.insert(END,arme)
      for lieu in self.cluedoLieu:
        self.listboxLieu.insert(END,lieu)
      self.listboxSuspect.grid(row=0,column=0)
      self.listboxArme.grid(row=0,column=2)
      self.listboxLieu.grid(row=0,column=4)

      Button(self.modifCluedoWindow,text="Add Suspect",command=self.addSuspect).grid(row=1,column=0,columnspan=1,sticky="EW")
      Button(self.modifCluedoWindow,text="Add Weapon",command=self.addArme).grid(row=1,column=1,columnspan=2,sticky="EW")
      Button(self.modifCluedoWindow,text="Add Place",command=self.addLieu).grid(row=1,column=3,columnspan=4,sticky="EW")
      Button(self.modifCluedoWindow,text="Delete Suspect",command=self.delSuspect).grid(row=2,column=0,columnspan=1,sticky="EW")
      Button(self.modifCluedoWindow,text="Delete Weapon",command=self.delArme).grid(row=2,column=1,columnspan=2,sticky="EW")
      Button(self.modifCluedoWindow,text="Delete Place",command=self.delLieu).grid(row=2,column=3,columnspan=4,sticky="EW")

  def addSuspect(self):
    self.listToAdd = self.cluedoSuspect
    self.listName = "Suspect"
    self.addCluedoAttribut()
  def addArme(self):
    self.listToAdd = self.cluedoArme
    self.listName = "Weapon"
    self.addCluedoAttribut()
  def addLieu(self):
    self.listToAdd = self.cluedoLieu
    self.listName = "Place"
    self.addCluedoAttribut()

  def delSuspect(self):
    self.listboxToDel = self.listboxSuspect
    self.listToDel = self.cluedoSuspect
    self.listName = "Suspect"
    self.deleteCluedoAttribut()
  def delArme(self):
    self.listboxToDel = self.listboxArme
    self.listToDel = self.cluedoArme
    self.listName = "Weapon"
    self.deleteCluedoAttribut()
  def delLieu(self):
    self.listboxToDel = self.listboxLieu
    self.listToDel = self.cluedoLieu
    self.listName = "Place"
    self.deleteCluedoAttribut()

  def deleteCluedoAttribut(self):
    """
    Suppression d'un attribut Cluedo
    """
    elemToDel = self.listboxToDel.index(ACTIVE)
    if elemToDel == None:
      showerror("Error","You have to select a {} to remove".format(self.listName))
    else:
      if len(self.listToDel)==1:
        showerror("Error","You need atleast 1 possibility")
      else:
        showinfo("Removed","{} is not a {} anymore".format(self.listToDel[elemToDel],self.listName))
        del self.listToDel[elemToDel]
        self.modifCluedoWindow.destroy()
        self.modifCluedo()

  def addCluedoAttribut(self):
    """
    Fenetre d'ajout de nouvelle attribut
    """
    try:
      self.addCluedoWindow.destroy()
    except:
      pass
    finally:
      self.addCluedoWindow = Toplevel()
      self.addCluedoWindow.title("Add attribut")
      self.addCluedoWindow.resizable(False,False)
      Label(self.addCluedoWindow,text="Enter the new {} :".format(self.listName)).grid(row=0,column=0)
      newAttribut = StringVar()
      self.attributEntry = Entry(self.addCluedoWindow,textvariable=newAttribut)
      self.attributEntry.focus_set()
      self.attributEntry.selection_range(0,END)
      self.attributEntry.grid(row=0,column=1)
      Button(self.addCluedoWindow,text="Add",command=self.newCluedoAttribut).grid(row=0,column=2)
      self.addCluedoWindow.bind("<Return>",self.newCluedoAttribut)

  def newCluedoAttribut(self,event=0):
    """
    Ajoute un attribut au Cluedo
    """
    if self.attributEntry.get() in self.listToAdd:
      showerror("Error","You can't use it twice")
    else:
      self.listToAdd.append(self.attributEntry.get())
      try:
        self.addCluedoWindow.destroy()
        self.modifCluedoWindow.destroy()
      except:
        pass
      finally:
        self.modifCluedo()
      
#=====================================================
  
if __name__ == "__main__":
    root = Tk()
    app = GUI(root)
    app.mainloop()

#Ajouter le clique droit avec Cluedo
