% régression linéaire 

% création du modèle :
model = @(param, x) param(1) * x + param(2);


% génération des données :
x = linspace(-5, 15, 120);
y = 4.5 * x + 12 + randn(size(x));



% fit :
p = metropolis(model, x, y, [5, 10], [0.5, 1], 2000);


% moyennes et écarts types :
a = mean(p(500:end, 1));
da = std(p(500:end, 1));
b = mean(p(500:end, 2));
db = std(p(500:end, 2));

disp(["pente = ", num2str(a), " +- ", num2str(da)]);
disp(["ordonnée à l'origine = ",num2str(b) " +- ", num2str(db)]);

