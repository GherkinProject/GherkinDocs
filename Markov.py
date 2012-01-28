Markovienne = {}


u = ['Bonjour', 'Hallo', 'Bonne rencontre','The Rakes','Gherkin PGM']

for i in u:
    Markovienne[i] = {}
    for j in u:
        Markovienne[i][j]= float(len(i)+len(j))
for i in u:
    X = 0
    for j in u:
        X += Markovienne[i][j]
    for j in u:
        Markovienne[i][j] = Markovienne[i][j]/X



print Markovienne
print Markovienne['Bonjour']
