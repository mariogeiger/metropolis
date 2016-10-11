% résonance

% création du modèle :
model = @(p, x) p(1) * x ./ sqrt((p(2)^2 - x.^2).^2 + 4*p(3)^2 * x.^2);


% changement des données :
data = load("data");


% fit :
p = metropolis(model, data(:,1), data(:,2), [1000, 20e3, 1e3], [300, 5e3, 0.3e3], 50000);


% moyennes et écarts types :
q = floor(0.3*size(p, 1));

w0 = mean(p(q:end, 2));
dw0 = std(p(q:end, 2));

disp(["pulsation propre = ", num2str(w0), " +- ", num2str(dw0), " rad/s"]);
