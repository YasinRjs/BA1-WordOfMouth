#ARSLAN Yasin
#BA1 Science Info
#Projet d'année : Rumeur

"""
   Ce fichier contient toutes les fonctions utilisé dans le main.
   Qui se trouve dans le fichier rumor.py .
"""

from random import random
from random import randint
import argparse

#=========================
def LoadNetwork(filename):
#=========================
  """
     Chargement de la liste des noms et la matrice réseau 
     via un fichier texte donné en argument.
  """
  #Ouverture du fichier avec les relations.
  #Et lecture des lignes.
  f = open(filename)
  texte = f.readlines()
  f.close()
  print("------------The Network---------------")
  users = []
  friend = []
  
  for elem in texte:
    #Améliorer l'affichage.
    print(elem.strip())
    #Séparer la personne et ses amis.
    elem = elem.split(":")
    #Ajouter les éléments dans les listes distingues.
    users.append(elem[0].strip())
    friend.append(elem[1].strip())
  #Améliorer l'affichage.
  print()
  numberUsers = len(users)
  network = [[False for i in range(numberUsers)]for j in range(numberUsers)]
  
  #On ne suppose plus qu'une personne est ami avec elle même
  #pour alléger plusieurs partie du code.
  for i in range(numberUsers):
    #Une liste et non une chaine de charactère pour l'utilisation " in ".
    #Possibilité d'erreur avec chaine de characteres ( "Bob, Bobette" ).
    friends = [relation.strip() for relation in friend[i].split(",")]
    for j in range(numberUsers):
      if users[j] in friends:
        network[i][j] = True
  
  return (users,network)

#==================
def createParser():
#==================
  """
  Initialisation des possibles arguments."""
  parser = argparse.ArgumentParser(description="Social network")
  parser.add_argument("filename",help="Load network file ")
  parser.add_argument("-s","--rumorStarter",type=str, help="Rumor creator")
  parser.add_argument("-r","--initialRumor",type=int,default=randint(NUL,MAXVALUE-1), help="Initial rumor: Positive number from 0 to 255. A random from it by default.")
  parser.add_argument("-t","--timeSimule",type=int,default=EVERYONEMUSTKNOW,help="Positive integer.Steps of simlation. Stops when everyone knows the rumor by default.")
  parser.add_argument("-d","--dontTellAgain",action="store_true",default=False, help="Don't tell the rumor to a person who knows")
  #Pas besoin de valeur par défault pour celui-ci . Fonction modif() a été codé expressement pour ça.
  parser.add_argument("-m","--modification",type=str,choices={"incremental","bitflip","none"},default="none", help="Type of modification: incremental,bitfip or none. none by default")
  parser.add_argument("-p","--probability",type=float, default=DEFAULTPROBABILITY,help="Probability of modification. 1/10 by default.")
  parser.add_argument("-u","--update",type=str,default="stable",choices={"stable","rewrite","mixture"},\
   help="Update Rules: stable,rewrite,mixture. stable by default.")
  return parser.parse_args()

#====================
def verifyArgs(args):
#====================
  """
  Verifie les arguments tel que la rumeur est sur 24 bits, la probabilité entre 0.0 et 1.0
  et le temps de simulation, s'il est donné, est positif. """
  return args.initialRumor <= NUL or args.initialRumor > MAXVALUE-1 or args.probability < NUL or args.probability > MAXPROBABILITY \
  or (args.timeSimule != EVERYONEMUSTKNOW and not str(args.timeSimule).isdigit())

#=====================================
def PrintStates(users,informedPeople): 
#===================================== 
  """
     Fonction d'affichage : Connaissance de la rumeur.
  """
  for i in range(len(informedPeople)):
    if informedPeople[i] != dontKnow:
      print(users[i],"\t",informedPeople[i],"\t",int(informedPeople[i],2))
    else:
      print(users[i],"\t --doesn't know--")

#=================================================================
def create_rumor(users,informedPeople,initialPerson,initialRumor):
#=================================================================
  """
     Création de la rumeur donc modification d'informedPeople
     tel que la personne à la base de la rumeur connaisse la rumeur.
  """
  #Argument "-s X" provoque une création de la rumeur
  #A partir de la personne X. Sinon c'est aléatoire.
  if initialPerson!=None:
    if initialPerson in users:
      creator = users.index(initialPerson)
    else:
      raise Exception(" Rumor starter does not exist ")
  else:
    creator = randint(0,len(users)-1)

  print("Rumor starter : ",users[creator])
  #Randint(0,255) par défault, sinon l'entier à coté de l'argument -r.
  initial_rumor = "{:024b}".format(initialRumor)
  print("Initial rumor : ",int(initial_rumor,2))
  informedPeople[creator] = initial_rumor

#================================
def noModification(rumor_number):
#================================
  """
  Pas de modification.
  """
  return rumor_number

#=============================
def incremental(rumor_number):
#=============================
  """
  Prends un nombre en base 10 en paramaetre, l'incremente/decremente
  par rapport au random. Renvoie le nombre entre 0 et 255 compris
  """
  #Ecriture sur 24 bits.
  boolean = bool(randint(0,1))
  if boolean:
    rumor_number += 1
  else:
    rumor_number -= 1
  return (rumor_number%MAXVALUE)

#=========================  
def bitflip(rumor_number):
#=========================
  """
  Prends un nombre en base 10, le converti en binaire base 24.
  Choisi une indice aléatoire dans ce nombre binaire et le modifi.
  """
  indice = randint(0,NUMBERBITS-1)
  #Ecriture binaire
  bin_number = "{:024b}".format(rumor_number)
  #Pour ne pas faire de if else, méthode utilisé pour modifier le bit choisi.
  bin_number = bin_number[:indice] + str(int(not(int(bin_number[indice])))) + bin_number[indice+1:]
  return int(bin_number,2)

#===========================
def modif(rumor,modifRules):
#===========================
  """
  Vérification de la demande voulu, soit la rumeur se modif.
  de maniere incremental , bitflip, ou sans modification.
  """
  modifFunction = modificationDict[modifRules]
  rumor = modifFunction(rumor)
  return rumor

#=============================================
def simule(users,network,informedPeople,args):
#=============================================
  """
  Vérification de la demande voulu, soit tout le monde 
  doit connaitre la rumeur, soit nombre d'étapes.
  """
  timeSimule = args.timeSimule
  continuePropagation = timeSimule != 0
  knowsRumor = 1
  step = 0
  #Simulation de la rumeur en fonction du nombre d'étapes.
  while continuePropagation:
    step+=1
    print("### Simulation step : ",step)
    learn_step = update(users,network,informedPeople,args)
    print("-->",learn_step,"learned the rumor this step")
    PrintStates(users,informedPeople)
    knowsRumor += learn_step
    if timeSimule == EVERYONEMUSTKNOW :
      continuePropagation = (knowsRumor < len(users))
    else:
      continuePropagation = step<timeSimule

#================================
def stable(rumor,chosenOneRumor):
#================================
  res = rumor
  #int au cas où 000000000 rumeur.
  if chosenOneRumor != NUL:
    res = chosenOneRumor
  return res

#=================================
def mixture(rumor,chosenOneRumor):
#=================================
  probability_change = 0.1 #10%
  number_bits = 24

  rumor = "{:024b}".format(rumor)
  base_rumor = "{:024b}".format(chosenOneRumor)
  if base_rumor != dontKnow:
    new_rumor = ""
    for j in range(number_bits):
      if base_rumor[j] == rumor[j]:
        new_rumor += base_rumor[j]
      else:
        prob = round(random(),1)
        if prob == probability_change:
          new_rumor += base_rumor[j]
        else:
          new_rumor += rumor[j]
  else:
    new_rumor = rumor
  
  return int(new_rumor,2)

#=================================
def rewrite(rumor,chosenOneRumor):
#=================================
  return rumor

#=======================================================
def updateRules(newInformed,rumor,chosenOne,updateRule):
#=======================================================
  """
  Les types de mise à jour possible. Stable par default,
  rewrite, mixture.
  """

  updateFunction = updateDict[updateRule]
  chosenOneRumor = newInformed[chosenOne]
  newRumor = updateFunction(int(rumor,2),int(chosenOneRumor,2))
  newInformed[chosenOne] = "{:024b}".format(newRumor)
  newInformed[:] = newInformed

#=============================================
def update(users,network,informedPeople,args):
#=============================================
  """
     Mise à jour du réseau. Chaque personne connaissant la
     rumeur ce tour va la transmettre à un ami autre que lui même.
     Cette fonction retourne le nombre de personne ayant appris la
     rumeur
  """

  #Liste des personnes aux courant.
  newInformed = informedPeople[:]
  numberOfnewinformedPeople = 0
  #Active ou non de -Don't tell again.
  #Mise dans une variable pour ne pas faire de recherche dans args à chaque tour.
  flag = args.dontTellAgain
  probability_change = args.probability
  for i in range(len(informedPeople)):
    rumor = informedPeople[i]
    if rumor != dontKnow:
      if flag:
        friends = [j for j in range(len(network)) if network[i][j] and newInformed[j] == dontKnow]
      else:
        friends = [j for j in range(len(network)) if network[i][j]]
      if len(friends)>NUL:
        #Proba_modif doit être un réel entre 0 et 1.
        proba_modif = random()
        #On autorise la probabilité donné en argument à avoir autant de nombre
        #après la virgule pour une probabilité defini précisement.
        if proba_modif <= probability_change:
          rumor = "{:024b}".format(modif(int(rumor,2),args.modification))
        chosenOne = randint(0,len(friends)-1)
        chosenOne = friends[chosenOne]

        if newInformed[chosenOne] == dontKnow:
          numberOfnewinformedPeople += 1
        
        updateRules(newInformed,rumor,chosenOne,args.update)
  
  informedPeople[:] = newInformed
  
  return (numberOfnewinformedPeople)
###########################################################################
#======================= Constantes et Globales =================================
EVERYONEMUSTKNOW = -1
NUMBERBITS = 24
MAXVALUE = 2**NUMBERBITS
DEFAULTPROBABILITY = 0.1
MAXPROBABILITY = 1
NUL = 0
modificationDict = {"none":noModification,"incremental":incremental,"bitflip":bitflip}
updateDict = {"stable":stable,"rewrite":rewrite,"mixture":mixture}
dontKnow = "0"*NUMBERBITS
#=================================================================================
