from numba import jit
import numpy as np
import time


var = 1
if type(var) == float:
   print('your variable is an integer')

SQRT_2PI = np.sqrt(2 * np.pi)

@jit(nopython=True, parallel=True)
def gaussians(x, means, widths):
    '''Return the value of gaussian kernels.
    
    x - location of evaluation
    means - array of kernel means
    widths - array of kernel widths
    '''
    n = means.shape[0]
    result = np.exp( -0.5 * ((x - means) / widths)**2 ) / widths
    return result / SQRT_2PI / n

means = np.random.uniform(-1, 1, size=1000000)
widths = np.random.uniform(0.1, 0.3, size=1000000)


# normal case
start = time.time()
gaussians_nothread = jit(nopython=True, parallel = False)(gaussians.py_func)
gaussians_nothread(0.4, means, widths)
end = time.time()
print("Elapsed normal case = %s" % (end - start))

# DO NOT REPORT THIS... COMPILATION TIME IS INCLUDED IN THE EXECUTION TIME!
start = time.time()
gaussians(0.4, means, widths)
end = time.time()
print("Elapsed (with compilation) = %s" % (end - start))

# NOW THE FUNCTION IS COMPILED, RE-TIME IT EXECUTING FROM CACHE
start = time.time()
gaussians(0.4, means, widths)
end = time.time()
print("Elapsed (after compilation) = %s" % (end - start))


