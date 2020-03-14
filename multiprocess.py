import numpy as np
import numba
from numba import jit
import timeit

  
mysetup = '''
import numpy as np
import numba
from numba import jit
'''



# means = np.random.uniform(-1, 1, size=1000000)
# widths = np.random.uniform(0.1, 0.3, size=1000000)

# gaussians_nothread = jit(nopython=True)(gaussians.py_func)

mycode = '''
SQRT_2PI = np.sqrt(2 * np.pi)
@jit(nopython=True, parallel=True)
def gaussians(x, means, widths):
    n = means.shape[0]
    result = np.exp( -0.5 * ((x - means) / widths)**2 ) / widths
    return result / SQRT_2PI / n
means = np.random.uniform(-1, 1, size=1000000)
widths = np.random.uniform(0.1, 0.3, size=1000000)
gaussians_nothread = jit(nopython=True)(gaussians.py_func)
gaussians_nothread(0.4, means, widths)
'''

testcode = '''
SQRT_2PI = np.sqrt(2 * np.pi)
@jit(nopython=True, parallel=True)
def gaussians(x, means, widths):
    n = means.shape[0]
    result = np.exp( -0.5 * ((x - means) / widths)**2 ) / widths
    return result / SQRT_2PI / n
means = np.random.uniform(-1, 1, size=1000000)
widths = np.random.uniform(0.1, 0.3, size=1000000)
gaussians(0.4, means, widths)
'''

# timeit statement 
print (timeit.timeit(setup = mysetup, 
                     stmt = mycode, 
                     number = 100))
print (timeit.timeit(setup = mysetup, 
                     stmt = testcode, 
                     number = 100))


print("done")