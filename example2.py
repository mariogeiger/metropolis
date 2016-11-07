# -*- coding: utf-8 -*-
# résonance
from metropolis import metropolis
import numpy as np
import matplotlib.pyplot as plt

# création du modèle :
def model(p, x):
	return p[0] * x / np.sqrt((p[1]**2 - x**2)**2 + 4*p[2]**2 * x**2)


# chargement des données :
data = np.loadtxt("data")
x = data[:,0]
y = data[:,1]

# choix des paramètres initiaux
p_init = [1000, 25e3, 1e3]
plt.subplot(221)
plt.plot(x, y, 'o')
x_ = np.linspace(np.min(x), np.max(x), 1000)
plt.plot(x_, model(p_init, x_), '-')
plt.title("initial guess")

# p_var : in python, this parameter is only used to initialize the walkers.
#         then you can put small values when you are sure about the p_init.
p_var  = [500, 1e3, 0.5e3]

# fit :
p = metropolis(model, x, y, p_init, p_var, 10000, 4000)


# moyennes et écarts types :
w0 = np.mean(p[:,1]);
dw0 = np.std(p[:,1]);

print "pulsation propre = {} +- {}".format(w0, dw0)

# plots
plt.subplot(222)
plt.plot(x, y, 'o')
x_ = np.linspace(np.min(x), np.max(x), 1000)
plt.plot(x_, model(np.mean(p, axis=0), x_), '-')
plt.title("fit")

plt.subplot(223)
plt.hist(p[:,1], bins=20)
plt.title("distribution of w0")

plt.subplot(224)
plt.hist(p[:,2], bins=20)
plt.title("distribution of lambda")

plt.show()

