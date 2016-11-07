# -*- coding: utf-8 -*-
# régression linéaire
import metropolis
import numpy as np
import matplotlib.pyplot as plt

# création du modèle :
def model(p, x):
	return p[0] * x + p[1]

# génération aléatoire des données :
x = np.linspace(-5, 15, 30)
y = 4.5 * x + 12 + 2 * np.random.randn(len(x))

# fit :
p = metropolis.metropolis(model, x, y, [5, 10], [0.5, 1])

# moyennes et écarts types :
a  = np.mean(p[:,0], axis=0)
da = np.std( p[:,0], axis=0)
b  = np.mean(p[:,1], axis=0)
db = np.std( p[:,1], axis=0)

print "pente = {} +- {}".format(a, da)
print "ordonnée à l'origine = {} +- {}".format(b, db)

# plots
plt.figure()
plt.plot(x, y, 'o')
x_ = np.linspace(-6, 16, 1000)
plt.plot(x_, model(np.mean(p, axis=0), x_), '-')
plt.show()
