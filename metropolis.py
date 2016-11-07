import numpy as np
import emcee
from math import log

def metropolis(model, x, y, p_init, p_var, Niter=1000, Ninit=300, Nwalkers=10):
	def lnprob(p, x, y, model):
		# prior (sigma is nonnegative)
		if p[0] < 0:
		    return -np.inf
		# log of likelihood
		return - 0.5 * x.shape[0] * log(abs(p[0])) \
		       - np.sum(np.power(y - model(p, x), 2)) / (2 * p[0] ** 2)
	
	# choose initial parameters for each walker
	p0 = [np.append(np.random.rand(1) * np.std(y), p_init + np.random.rand(len(p_var)) * p_var) for i in range(Nwalkers)]
	
	# create emcee main object
	sampler = emcee.EnsembleSampler(Nwalkers, len(p_init) + 1, lnprob, args=[x, y, model])
	
	# run `Ninit` steps to initialize
	pos, prob, state = sampler.run_mcmc(p0, Ninit)
	sampler.reset()
	
	# run `Niter` steps
	sampler.run_mcmc(pos, Niter)
	
	
	return sampler.flatchain
