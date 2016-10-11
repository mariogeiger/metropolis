% plot de la marche aléatoire

% création du modèle :
model = @(param, x) param(1) * x + param(2);


% génération des données :
x = linspace(-5, 15, 120);
y = 4.5 * x + 12 + randn(size(x));



% fit :
figure
p = metropolis(model, x, y, [5, 10], [0.1, 0.2], 50000);


% plot de la marche aléatoire 
q = floor(0.3 * size(p,1));

figure
% dessine les q premiers points en rouge
plot(p(1:q, 1), p(1:q, 2), 'rx-', p(q+1:end, 1), p(q+1:end, 2), 'bx-');

% ce plot permet d'observer la correlation entre les paramètres
