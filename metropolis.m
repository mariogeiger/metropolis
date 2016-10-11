% hypothèse
%  y = model(T, x) + sigma * randn()
%
% étant donnés un modèle et un ensemble de mesures (X et Y)
% cherche T et sigma
% 
function [p,sig,x2,y2] = metropolis(model, X, Y, p_init, p_var, iter)

% valeurs par défaut
if nargin < 5
	p_var = 0.15 * p_init;
end
if nargin < 6
	iter = 5000;
end

% p doit être en format ligne
p_init = reshape(p_init, 1, numel(p_init));
p_var  = reshape(p_var,  1, numel(p_init));

N = length(X);

% valeurs qui seront sauvée pour chaque pas
p = zeros(iter, numel(p_init)); % paramètres du modèle
sig = zeros(iter, 1); % erreur de mesure

p(1,:) = p_init;
sig(1) = std(Y);
res_old = sum((Y - model(p(1,:), X)).^2) / (2 * sig(1)^2);

for i = 2:iter
	% variation aléatoire des paramètres et de l'erreur de mesure
	r = 2 * rand(size(p_var)) - 1;
	r = r .^ 3;
	p_new = p(i-1,:) + p_var .* r;
	sig_new = sig(i-1) * (1/1.1 + rand() * (1.1 - 1/1.1));

	res_new = sum((Y - model(p_new, X)).^2) / (2 * sig_new^2);
	
	% effectue le nouveau pas
	if rand() < exp(res_old - res_new) * (sig(i-1) / sig_new)^N
		res_old = res_new;
		p(i,:)  = p_new;
		sig(i)  = sig_new;
	else
		p(i,:) = p(i-1,:);
		sig(i) = sig(i-1);
	end
end

% terminé : on fait des plots
q = floor(0.3*iter);

x2 = linspace(X(1), X(end), max(1000, N));
y2 = model(mean(p(q:end,:)), x2);

nplot = numel(p_init) + 2;
n1 = floor(sqrt(nplot));
n2 = ceil(nplot / n1);

for i = 1:numel(p_init)
	subplot(n1, n2, i);
	hist(p(q:end,i), 30);
	xlabel(['parameter ',num2str(i)]);
end

subplot(n1, n2, nplot-1);
hist(sig(q:end), 30);
xlabel('sigma');

subplot(n1, n2, nplot);
plot(X,Y, 'o', x2,y2, '-');
legend('data', 'fit');

end
