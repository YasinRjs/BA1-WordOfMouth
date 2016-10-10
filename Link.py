
class Link:
  """
  Classe graphique Link.
  Trace une ligne principale représentant le noeud survolé en rouge.
  Trace des lignes secondaires représentant ses amis en bleu.
  """
  BASEDGE = 2
  DIVEDGE = 5
  MAINLINE = "#FF0000"
  OTHERLINE = "#001099"
  def __init__(self,other,base):
    self.lineWidth = self.BASEDGE + other.valueEdge.get()/self.DIVEDGE
    self.mainLink(other,base)
    self.friendsLink(other,base)
    
  def mainLink(self,other,base):
    """
    Trace la ligne principale de la personne survolé en rouge
    """
    self.mainline = other.networkFrame.create_line\
    (base.middle,other.networkFrame.middle,fill=self.MAINLINE,width=self.lineWidth)

  def friendsLink(self,other,base):
    """
    Trace la ligne bleu pour chaque ami de la personne survolé
    """
    for friend in base.friends:
      other.networkFrame.create_line(friend.middle,other.networkFrame.middle,\
        fill=self.OTHERLINE,width=self.lineWidth)
