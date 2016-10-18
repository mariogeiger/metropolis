# metropolis

## Example

```matlab
p = metropolis(@(param, x) param(1)+param(2)*x, (1:100), rand(1,100), [0,0], [1,1], 20000);
figure
plot(p(:,1), p(:,2), 'x')
```

Le code précédent cherche la meilleure droite qui approxime des nombre générés aléatoirement.
Le plot montre le parcours empunté par l'algorithme de metropolis dans l'espace des paramètres.
Grace aux propriétés de l'algorithme de metropolis, le plot montre le corélation entre les deux paramètres.

## Algorithme de Metropolis

Il permet de distribuer une chaine de nombre aléatoire `x_i` selon une loi de probabilité `P(x)` a condition de lui donner le ratio `P(x_i) / P(x_j)`.

Il faut choisir une densité `g(x_j | x_i)` permettant de générer aléatoirement un `x_j` à partir d'un `x_i`.

Il faut commencer par choisir une valeur de départ : `x_0`.
A partir de `x_i` générer un candidat `x'` avec probabilité `g(x' | x_i)`.
Puis calculer 
```
        P(x') g(x_i | x')
ratio = ------------------
        P(x_i) g(x' | x_i)
```
Prendre alors `x_i+1 = x'` avec probabilité `ratio` sinon prendre `x_i+1 = x_i`

Pour simplifier le calcul de `ratio` on peut prendre un `g` tel que `g(x' | x) = g(x | x')`.

Les `x_i` seront alors distribués selon la loi `P(x)`.

## Théorème de Bayes

`P(A|B) = P(A inter B) / P(B)`

Dans le cadre d'un fit de fonction, on définit `D` les mesures, `T` les paramètres du modèle. Alors en utilisant le théorème de Bayes on obtient
```
           P(D | T)  P(T)
P(T | D) = --------------
                P(D)
```

## Algorithme de fit

On combine les deux idées et on obtient comme `ratio` (`g` symmetrique) :

```
         P(D | T')  P(T')
ratio = ------------------
        P(D | T_i)  P(T_i)
```

La probabilité `P(T)` a une drôle d'interpretation, c'est la probabilité d'obtenir les paramètres `T` sans connaitre la mesure. Dans la majorité des cas on peut considérer que `P(T_j) = P(T_i)`.

## Calcul du ratio

Pour calculer `P(D | T') / P(D | T_i)` dans le cas d'un fit avec comme mesures `(X,Y)` on peut prendre comme hypothèse que 
```
Y = model(X, T) + sigma randn
```
Où `model` est une fonction théorique qui permet de calculer les `Y` en fonction des `X` est des paramètres `T`.
On a modelisé l'erreur de mesure à l'aide d'une distribution normale de variance `sigma^2`

On peut alors calculer `P(D | T)`

```
              n                                                  n           1               1   Y_i - model(X_i, T)
P(D | T) = produit P(Y_i = model(X_i, T) + sigma randn | T) = produit --------------- exp(- --- (-------------------)^2)
            i = 1                                              i = 1  sigma sqrt(2pi)        2         sigma
            
           1                    1        n                                        1                   R
= ------------------- exp(- --------   somme (Y_i - model(X_i, T))^2) == ------------------- exp(- --------)
  sigma^N sqrt(2pi)^N       2sigma^2   i = 1                             sigma^N sqrt(2pi)^N       2sigma^2
```

En en déduit le ratio :

```
         P(D | T')    sigma_i           R_i           R'
ratio = ---------- = (-------)^N exp(---------- - ---------)
        P(D | T_i)    sigma'         2sigma_i^2   2sigma'^2
```

(Ce résultat est utilisé à la ligne 41 du script)

Référence : Le raisonnement bayésien: Modélisation et inférence
