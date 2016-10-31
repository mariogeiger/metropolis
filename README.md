# metropolis

## Example

```matlab
p = metropolis(@(param, x) param(1)+param(2)*x, (1:100), rand(1,100), [0,0], [1,1], 20000);
figure
plot(p(:,1), p(:,2), 'x')
```

Le code précédent cherche la meilleure droite qui approxime des nombre générés aléatoirement.
`p` contient une marche aléatoire des différents paramètres.
Le plot montre le parcours empunté par l'algorithme de metropolis dans l'espace des paramètres.
Grace aux propriétés de l'algorithme de metropolis, le plot montre la corélation entre les deux paramètres.

Pour donner une valeur et une insertitude aux paramètres il suffit de calculer la moyenne (`mean(p(500:end,:))`) et l'écart type (`std(p(500:end,:))`) de la queue de la marche aléatoire (`p`).

Voir aussi les fichier d'examples :
- `example1.m` : Fit des données générées aléatoirement à l'aide d'une fonction affine puis calcule la moyenne et l'écart type des paramètres du fit.
- `example2.m` : Fit des données mesurées (fichier `data`) à l'aide de la bonne fonction théorique pour en déduire la valeur de la fréquence propre avec une insertitude.
- `example3.m` : Montre le chemin emprunté par les itérations de l'algorithme, les première itérations sont transitoire puis le système se stabilise ce qui permet de déduire les distribution des paramètres (variance, covariances, ...)

## Paramètres et retour de la fonction

1. Le modèle qui lie x à y en fonction des paramètres : une fonction qui prend en arguments un vecteur représentant les paramètres et un vecteur représentant les valeurs x
2. Les données mesurées en x
3. Les données mesurées en y
4. Les paramètres initiaux (c'est via ce paramètre que l'algorithme sait combien il y a de paramètres)
5. La taille maximale des pas de la marche aléatoire selon chaque paramètres
5. Le nombre d'itérations

Retourne une matrice de taille (nombre d'iteration) x (nombre de paramètres).
Chaque ligne correspond à un pas de la marche aléatoire.
Si l'on retire la période transitoire, chaque ligne est distribuée aléatoirement selon "la bonne distribution".

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

On combine les deux idées : l'objectif est de distribuer une suite `T_i` selon la probabilité `P(T | D)`.

En prenant une fonction `g` symétrique, on obtient comme ratio :

```
         P(D | T')  P(T')
ratio = ------------------
        P(D | T_i)  P(T_i)
```

La probabilité `P(T)` a une drôle d'interpretation, c'est la probabilité d'obtenir les paramètres `T` sans connaitre la mesure. Dans la majorité des cas on peut considérer que `P(T_j) = P(T_i)`.

## Calcul du ratio

Pour calculer `P(D | T') / P(D | T_i)` dans le cas d'un fit avec comme mesures `(X,Y)` on prend comme hypothèse que les mesure suivent la loi suivante :
```
Y = model(X, T) + sigma N
```
Où `model` est une fonction déterministe (propre au problème étudié) qui permet de calculer les `Y` en fonction des `X` est des paramètres `T`.
`N` est une variable aléatoire distribuée selon la loi normale.

On peut alors calculer `P(D | T)`

```
              n
P(D | T) = Produit P(Y_i = model(X_i, T) + sigma randn | T)
            i = 1
            
     n           1               1   Y_i - model(X_i, T)
= Produit --------------- exp(- --- (-------------------)^2)
   i = 1  sigma sqrt(2pi)        2         sigma
            
           1                  n   (Y_i - model(X_i, T))^2
= ------------------- exp(- Somme -----------------------)
  sigma^n sqrt(2pi)^n       i = 1       2 sigma^2
```

Si on définit les résidus `R` comme
```
      n   (Y_i - model(X_i, T))^2
R = Somme -----------------------
    i = 1       2 sigma^2
```

En en déduit le ratio :

```
         P(D | T')    sigma_i
ratio = ---------- = (-------)^n exp(R_i - R')
        P(D | T_i)    sigma'
```

(Ce résultat est utilisé à la ligne 41 du script)

Référence : Le raisonnement bayésien: Modélisation et inférence
