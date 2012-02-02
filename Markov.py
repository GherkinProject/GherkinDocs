import random

class Markovienne():

    def __init__(self):
        self.markov = {}
        self.number = {}
        self.dbName = 'ProcessOfMarkov.ghk'
# markov fait office de dictionnaire de dictionnaire. 
# En realite c est une matrice, tel que self.markov de i et j represente la proba de transition de l artiste i a l artiste j
# nombre[i] enfin recense le nombre de vote/ de load que l on d un artiste a un autre.
# si je passe de twostepfromhell a LOTR jincremente nombre[twostepfromhell]

    def create_Markov(self, artistList):
        """Creer un fichier .ghk avec les proba de transition"""
        file = open(self.dbName, 'w')        
        for i in artistList:
            self.markov[i] = {}
            self.number[i] = 0.0
            for j in artistList:
                self.markov[i][j] = 0.0
                file.write(i + "$" + j + "$" + str(self.markov[i][j])+ '$' + str(self.number[i])+ '$')
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
        """ Sauvegarde les données"""
        file = open(self.dbName, 'w')
        for i in self.markov.keys():
            for j in self.markov[i].keys():
                file.write(i + "$" + j + "$" + str(self.markov[i][j])+ '$' + str(self.number[i])+ '$')
                file.write('\n')
        file.close()
			
    def vote_Markov(self, artistBeginning, artistEnd):
        """ Realise le vote du passage entre artistBeginning et artistEnd"""
        self.number[artistBeginning]+=1
        for j in self.markov[artistBeginning].keys():
            if j == artistEnd:
                self.markov[artistBeginning][j] = (self.markov[artistBeginning][j]*(self.number[artistBeginning]-1)+1)/(self.number[artistBeginning])
            else:
                self.markov[artistBeginning][j] *= (self.number[artistBeginning]-1)/(self.number[artistBeginning])
        
    def choix_Markov(self, artist):
        """ choisi le successeur de l artiste entrain d etre joue"""
        u = random.random() # nombre aleatoire entre 0 et 1
        for k in self.markov[artist].keys():
            if self.markov[artist][k] >= u:
# dans ce cas la chaine de markov nous indique que le prochain artiste sera k
                return k
            else:
# sinon on regarde les autres artistes, en decrementant u. on trouve techniquement qu il y a toujours un k renvoye si u != 1
                u -= self.markov[artist][k]





L = ["Boris","Gautier","Nico","Plate-voute"]
U = Markovienne()
U.create_Markov(L)
for u in range(15):
    U.vote_Markov("Gautier","Nico")
    U.vote_Markov("Nico","Boris")
for u in range (4):
    U.vote_Markov("Gautier","Boris")
    U.vote_Markov("Nico","Gautier")

print U.markov

print U.choix_Markov("Gautier")

U.save_Markov()
file = open('ProcessOfMarkov.ghk','r')
print file.read()
