from rumorFunctions import *

def main():
  
  args = createParser()
  try:
    users,network = LoadNetwork(args.filename)
  except IOError:
    print("#-- {} --# isn't in the directory.".format(args.filename))
  except IndexError:
    print("A line of #-- {} --# is badly written.".format(args.filename))
  except:
    print("Unkown error.")
  else:
    if len(users)>NUL:
      informedPeople = [dontKnow for i in range(len(users))]
      if verifyArgs(args):
        print("#ERROR# ---- Check your arguments ----")
      else:
        #Une personne de la liste des utilisateurs apprends la rumeur.
        #Uniquement cette personne connait la rumeur à l'état initial.
        #Affichage de l'état initial de la rumeur.
        create_rumor(users,informedPeople,args.rumorStarter,args.initialRumor)
        print("###\nInitial :")
        PrintStates(users,informedPeople)

        simule(users,network,informedPeople,args)
        print("--- End of Simulation ---")

    else:
      #Fichier d'intruction vide.
      print("Your network has no succes, You have 0 users ! Haha")
#####################################################################

if __name__ == "__main__":
  main()

