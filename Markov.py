import random

class Markovienne():

    def __init__(self, dbName= "ProcessOfMarkov"):
        self.markov = {}
        self.number = {}
        self.dbName = dbName
# markov fait office de dictionnaire de dictionnaire. 
# En realite c est une matrice, tel que self.markov de i et j represente la proba de transition de l songe i a l songe j
# nombre[i] enfin recense le nombre de vote/ de load que l on d un songe a un autre.
# si je passe de twostepfromhell a LOTR jincremente nombre[twostepfromhell]

    def create_Markov(self, songList):
        """Creer un fichier .ghk avec les proba de transition"""
        file = open(self.dbName, 'w')        
        for i in songList:
            self.markov[i] = {}
            self.number[i] = 0.0
            for j in songList:
                self.markov[i][j] = 1.0 / float(len(songList))
                file.write(str(i) + "$" + str(j) + "$" + str(self.markov[i][j])+ '$' + str(self.number[i])+ '$')
                file.write('\n')
        file.close()

    def load_Markov(self, fileName):
        """ Charge le fichier .ghk contenant les probas de transition"""
        self.dbName = fileName
        file = open(self.dbName, 'r')
        for line in file:
            u = line.split('$')
            self.markov[u[0]][u[1]] = u[3]
            self.number[u[0]] = u[4]
        file.close()

    def save_Markov(self):
        """ Sauvegarde les donnees"""
        file = open(self.dbName, 'w')
        for i in self.markov.keys():
            for j in self.markov[i].keys():
                file.write(str(i) + "$" + str(j) + "$" + str(self.markov[i][j])+ '$' + str(self.number[i])+ '$')
                file.write('\n')
        file.close()
			
    def vote_Markov(self, songBeginning, songEnd):
        """ Realise le vote du passage entre songBeginning et songEnd"""
        self.number[songBeginning]+=1
        for j in self.markov[songBeginning].keys():
            if j == songEnd:
                self.markov[songBeginning][j] = (self.markov[songBeginning][j]*(self.number[songBeginning]-1)+1)/(self.number[songBeginning])
            else:
                self.markov[songBeginning][j] *= (self.number[songBeginning]-1)/(self.number[songBeginning])
        
    def choix_Markov(self, idSong):
        """ Choisit le successeur de song entrain d etre joue"""
        u = random.random() # nombre aleatoire entre 0 et 1
        for k in self.markov[idSong].keys():
            if self.markov[idSong][k] >= u:
# dans ce cas la chaine de markov nous indique que le prochain songe sera k
                return k
            else:
# sinon on regarde les autres songes, en decrementant u. on trouve techniquement qu il y a toujours un k renvoye si u != 1
                u -= self.markov[idSong][k]





