import numpy as np
import emcee

def metropolis(f, x, y, p_init, p_var, Niter=1000, Ninit=None, Nwalkers=10):
    if Ninit is None:
        Ninit = Niter // 2

    p_init = np.array(p_init, dtype=np.float64)
    p_var = np.array(p_var, dtype=np.float64)
    x = np.array(x, dtype=np.float64)
    y = np.array(y, dtype=np.float64)

    def lnprob(p, x, y, f):
        # prior : sigma is positive
        if p[0] <= 0:
            return -np.inf
        # log of likelihood
        return - x.shape[0] * np.log(p[0]) \
               - np.sum((y - f(x, *p[1:]))**2) / (2. * p[0] ** 2)

    # choose initial parameters for each walker
    p0 = [np.append(np.random.rand(1) * np.std(y), p_init + np.random.randn(len(p_var)) * p_var) for i in range(Nwalkers)]

    # create emcee main object
    sampler = emcee.EnsembleSampler(Nwalkers, len(p_init) + 1, lnprob, args=[x, y, f])

    # run `Ninit` steps to initialize
    pos, prob, state = sampler.run_mcmc(p0, Ninit)
    sampler.reset()

    # run `Niter` steps
    sampler.run_mcmc(pos, Niter)


    return sampler.flatchain[:, 1:]
