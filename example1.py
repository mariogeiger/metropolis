import metropolis
import numpy as np

# régression linéaire 


# création du modèle :
def model(p, x):
	# p[0] is used internaly
	return p[1] * x + p[2]

# génération aléatoire des données :
x = np.linspace(-5, 15, 120)
y = 4.5 * x + 12 + np.random.randn(len(x))

# fit :
p = metropolis.metropolis(model, x, y, [5, 10], [0.5, 1])


# moyennes et écarts types :
a  = np.mean(p[:,1], axis=0)
da = np.std( p[:,1], axis=0)
b  = np.mean(p[:,2], axis=0)
db = np.std( p[:,2], axis=0)

print "pente = {} +- {}".format(a, da)
print "ordonnee a l'origine = {} +- {}".format(b, db)
