# -*- coding: utf-8 -*-
# plot de la marche aléatoire
from metropolis import metropolis
import numpy as np
import matplotlib.pyplot as plt

# création du modèle :
def model(param, x):
	return param[0] * x + param[1]


# génération des données :
x = np.linspace(-5, 15, 120)
y = 4.5 * x + 12 + 5 * np.random.randn(len(x))



# fit :
p = metropolis(model, x, y, [5, 10], [0.1, 0.2], 5000, 500, 20)


# plot de la marche aléatoire
plt.figure()
plt.plot(p[:,0], p[:,1], 'x')
plt.title("{} points".format(p.shape[0]))
plt.xlabel("slope")
plt.ylabel("intercept")
plt.show()

# ce plot permet d'observer la correlation entre les paramètres
