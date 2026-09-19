"""random module for CustomPython OS.

Generate pseudo-random numbers.
"""

import math
import os


# Constants
VERSION = 3

# Period parameters
N = 624
M = 397
MATRIX_A = 0x9908B0DF
UPPER_MASK = 0x80000000
LOWER_MASK = 0x7FFFFFFF


class Random:
    """Random number generator."""
    
    def __init__(self, x=None):
        self._seed = 0
        self._mt = [0] * N
        self._index = N + 1
        if x is not None:
            self.seed(x)
    
    def seed(self, a=None, version=2):
        """Initialize the random number generator."""
        if a is None:
            try:
                a = int.from_bytes(os.urandom(4), 'big')
            except NotImplementedError:
                a = 0
        
        if version == 2:
            if isinstance(a, (str, bytes, bytearray)):
                if isinstance(a, str):
                    a = a.encode()
                a = int.from_bytes(a, 'big')
        
        self._mt[0] = a & 0xFFFFFFFF
        for i in range(1, N):
            self._mt[i] = (1812433253 * (self._mt[i-1] ^ (self._mt[i-1] >> 30)) + i) & 0xFFFFFFFF
        self._index = N
    
    def _genrand_int32(self):
        """Generate a random number on [0, 0xFFFFFFFF]-interval."""
        if self._index >= N:
            self._twist()
        
        y = self._mt[self._index]
        self._index += 1
        
        # Tempering
        y ^= (y >> 11)
        y ^= (y << 7) & 0x9D2C5680
        y ^= (y << 15) & 0xEFC60000
        y ^= (y >> 18)
        
        return y
    
    def _twist(self):
        """Generate the next N words from the state."""
        for i in range(N):
            x = (self._mt[i] & UPPER_MASK) | (self._mt[(i + 1) % N] & LOWER_MASK)
            self._mt[i] = self._mt[(i + M) % N] ^ (x >> 1)
            if x & 1:
                self._mt[i] ^= MATRIX_A
        self._index = 0
    
    def random(self):
        """Return a random float in [0.0, 1.0)."""
        return self._genrand_int32() / (2**32)
    
    def randint(self, a, b):
        """Return random integer in range [a, b]."""
        return a + int(self.random() * (b - a + 1))
    
    def randrange(self, start, stop=None, step=1):
        """Choose a random item from range(start, stop[, step])."""
        if stop is None:
            stop = start
            start = 0
        
        if step == 0:
            raise ValueError('step must not be zero')
        
        if step > 0:
            n = (stop - start + step - 1) // step
        else:
            n = (start - stop - step - 1) // (-step)
        
        if n <= 0:
            raise ValueError('empty range for randrange()')
        
        return start + self.randint(0, n - 1) * step
    
    def choice(self, seq):
        """Return a random element from the non-empty sequence seq."""
        if not seq:
            raise IndexError('cannot choose from an empty sequence')
        return seq[self.randint(0, len(seq) - 1)]
    
    def choices(self, population, weights=None, *, cum_weights=None, k=1):
        """Return a k-sized list of elements chosen from population with replacement."""
        import bisect
        
        if cum_weights is None:
            if weights is None:
                cum_weights = []
                total = len(population)
                for i in range(total):
                    cum_weights.append(i + 1)
            else:
                cum_weights = []
                total = 0
                for w in weights:
                    total += w
                    cum_weights.append(total)
        
        if not population:
            raise IndexError('cannot choose from an empty sequence')
        
        result = []
        for _ in range(k):
            n = len(cum_weights)
            total = cum_weights[-1]
            hi = n - 1
            x = self.random() * total
            lo = 0
            while lo < hi:
                mid = (lo + hi) // 2
                if x < cum_weights[mid]:
                    hi = mid
                else:
                    lo = mid + 1
            result.append(population[lo])
        
        return result
    
    def shuffle(self, x, random=None):
        """Shuffle list x in place."""
        if random is None:
            random = self.random
        
        for i in range(len(x) - 1, 0, -1):
            j = int(random() * (i + 1))
            x[i], x[j] = x[j], x[i]
    
    def sample(self, population, k, *, counts=None):
        """Return a k length list of unique elements chosen from the population."""
        if k > len(population):
            raise ValueError('sample larger than population')
        
        result = []
        for _ in range(k):
            idx = self.randint(0, len(population) - 1)
            result.append(population[idx])
            population = population[:idx] + population[idx+1:]
        
        return result
    
    def uniform(self, a, b):
        """Return a random floating point N such that a <= N <= b for a <= b."""
        return a + self.random() * (b - a)
    
    def triangular(self, low=0.0, high=1.0, mode=None):
        """Return a random floating point number N such that low <= N <= high."""
        u = self.random()
        if mode is None:
            mode = (low + high) / 2
        
        c = (mode - low) / (high - low)
        
        if u > c:
            u = 1.0 - u
            c = 1.0 - c
            low = high
            high = mode
        
        return low + (high - low) * math.sqrt(u * c)
    
    def gauss(self, mu, sigma):
        """Gaussian distribution."""
        # Box-Muller transform
        u1 = self.random()
        u2 = self.random()
        while u1 == 0:
            u1 = self.random()
        z = math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2)
        return mu + sigma * z
    
    def normalvariate(self, mu, sigma):
        """Normal distribution."""
        return self.gauss(mu, sigma)
    
    def lognormvariate(self, mu, sigma):
        """Log normal distribution."""
        return math.exp(self.gauss(mu, sigma))
    
    def expovariate(self, lambd):
        """Exponential distribution."""
        return -math.log(1.0 - self.random()) / lambd
    
    def vonmisesvariate(self, mu, kappa):
        """Circular uniform distribution."""
        if kappa == 0:
            return self.uniform(0, 2 * math.pi)
        
        u = self.random()
        z = math.cos(math.pi * u)
        d = z + kappa
        t = (1 + kappa * kappa) / (2 * kappa)
        
        while d <= 0 or math.log(d / t) > kappa * (1 - z):
            u = self.random()
            z = math.cos(math.pi * u)
            d = z + kappa
            t = (1 + kappa * kappa) / (2 * kappa)
        
        mu_val = mu + math.atan2(math.sin(math.acos(z)), kappa + z)
        return mu_val % (2 * math.pi)
    
    def gammavariate(self, alpha, beta):
        """Gamma distribution."""
        if alpha <= 0 or beta <= 0:
            raise ValueError('alpha and beta must be > 0')
        
        if alpha > 1:
            a = math.sqrt(2 * alpha - 1)
            b = alpha - math.log(4)
            c = alpha + a
            
            while True:
                u = self.random()
                if u == 0:
                    continue
                x = a * math.log(u / (1 - u))
                g = alpha * math.exp(x)
                r1 = c * x
                r2 = a * math.exp(x / 2)
                v = math.exp(math.log(g) + math.sin(x) - r1 - r2)
                if math.log(u) < math.log(g) - r1 - r2 + math.sin(x):
                    return g * beta
        else:
            while True:
                u = self.random()
                while u == 0:
                    u = self.random()
                y = math.log(u / (1 - u))
                x = alpha * math.exp(y)
                t = alpha * math.exp(y / 2) + 1
                v = math.exp(math.log(x) - y)
                if u < 1 - 0.0331 * (y * y) * (y * y):
                    return x * beta
                if math.log(u) < 0.5 * y * y + (1 + alpha) * math.log(t) - t + math.log(alpha):
                    return x * beta
    
    def betavariate(self, alpha, beta):
        """Beta distribution."""
        y = self.gammavariate(alpha, 1)
        if y == 0:
            return 0
        return y / (y + self.gammavariate(beta, 1))
    
    def paretovariate(self, alpha):
        """Pareto distribution."""
        u = 1 - self.random()
        return 1 / u ** (1 / alpha)
    
    def weibullvariate(self, alpha, beta):
        """Weibull distribution."""
        u = 1 - self.random()
        return alpha * (-math.log(u)) ** (1 / beta)
    
    def getstate(self):
        """Return internal state for pickling."""
        return (self._index, tuple(self._mt))
    
    def setstate(self, state):
        """Restore internal state from pickling."""
        index, mt = state
        self._index = index
        self._mt = list(mt)
    
    def getrandbits(self, k):
        """Return a random integer with k random bits."""
        result = 0
        for _ in range(k):
            result = (result << 1) | self.randint(0, 1)
        return result


# Global instance
_inst = Random()
seed = _inst.seed
random = _inst.random
uniform = _inst.uniform
randint = _inst.randint
randrange = _inst.randrange
choice = _inst.choice
choices = _inst.choices
shuffle = _inst.shuffle
sample = _inst.sample
gauss = _inst.gauss
normalvariate = _inst.normalvariate
lognormvariate = _inst.lognormvariate
expovariate = _inst.expovariate
vonmisesvariate = _inst.vonmisesvariate
gammavariate = _inst.gammavariate
betavariate = _inst.betavariate
paretovariate = _inst.paretovariate
weibullvariate = _inst.weibullvariate
getstate = _inst.getstate
setstate = _inst.setstate
getrandbits = _inst.getrandbits
triangular = _inst.triangular
