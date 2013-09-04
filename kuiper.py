
# By Anne M. Archibald, 2007
from numpy import copy, sort, amax, arange, exp, sqrt, abs, floor, searchsorted
from scipy import factorial
import itertools

def binomial(n, m):
    return factorial(n)/(factorial(m)*factorial(n-m))

def kuiper_FPP(D,N):
    """Compute the false positive probability for the Kuiper statistic

    Uses the set of four formulas described in Paltani 2004; they report the resulting function never underestimates the false positive probability but can be a bit high in the N=40..50 range. (They quote a factor 1.5 at the 1e-7 level.
    """
    if D<0. or D>2.:
        raise ValueError("Must have 0<=D<=2")

    if D<2./N:
        return 1. - factorial(N)*(D-1./N)**(N-1)
    elif D<3./N:
        k = -(N*D-1.)/2.
        r = sqrt(k**2 - (N*D-2.)/2.)
        a, b = -k+r, -k-r
        return 1. - factorial(N-1)*(b**(N-1.)*(1.-a)-a**(N-1.)*(1.-b))/float(N)**(N-2)*(b-a)
    elif (D>0.5 and N%2==0) or (D>(N-1.)/(2.*N) and N%2==1):
        def T(t):
            y = D+t/float(N)
            return y**(t-3)*(y**3*N-y**2*t*(3.-2./N)/N-t*(t-1)*(t-2)/float(N)**2)
        s = 0.
        # NOTE: the upper limit of this sum is taken from Stephens 1965
        for t in xrange(int(floor(N*(1-D)))+1):
            term = T(t)*binomial(N,t)*(1-D-t/float(N))**(N-t-1)
            s += term
        return s
    else:
        z = D*sqrt(N) 
        S1 = 0.
        term_eps = 1e-12
        abs_eps = 1e-100
        for m in itertools.count(1):
            T1 = 2.*(4.*m**2*z**2-1.)*exp(-2.*m**2*z**2)
            so = S1
            S1 += T1
            if abs(S1-so)/(abs(S1)+abs(so))<term_eps or abs(S1-so)<abs_eps:
                break
        S2 = 0.
        for m in itertools.count(1):
            T2 = m**2*(4.*m**2*z**2-3.)*exp(-2*m**2*z**2)
            so = S2
            S2 += T2
            if abs(S2-so)/(abs(S2)+abs(so))<term_eps or abs(S1-so)<abs_eps:
                break
        return S1 - 8*D/(3.*sqrt(N))*S2

def kuiper(data, cdf=lambda x: x):
    """Compute the Kuiper statistic
    
    Use the Kuiper statistic version of the Kolmogorov-Smirnov test to find the probability that something like data was drawn from the distribution whose CDF is given as cdf.

    The Kuiper statistic resembles the Kolmogorov-Smirnov test in that it is nonparametric and invariant under reparameterizations of the data. The Kuiper statistic, in addition, is equally sensitive throughout the domain, and it is also invariant under cyclic permutations (making it particularly appropriate for analyzing circular data). 

    Returns (D, fpp), where D is the Kuiper D number and fpp is the probability that a value as large as D would occur if data was drawn from cdf.

    Warning: The fpp is calculated only approximately, and it can be as much as 1.5 times the true value.

    Stephens 1970 claims this is more effective than the KS at detecting changes in the variance of a distribution; the KS is (he claims) more sensitive at detecting changes in the mean.

    If cdf was obtained from data by fitting, then fpp is not correct and it will be necessary to do Monte Carlo simulations to interpret D. D should normally be independent of the shape of CDF.
    """

    # FIXME: doesn't work for distributions that are actually discrete (for example Poisson).
    data = sort(data)
    cdfv = cdf(data)
    N = len(data)
    D = amax(cdfv-arange(N)/float(N)) + amax((arange(N)+1)/float(N)-cdfv)

    return D, kuiper_FPP(D,N)

def kuiper_two(data1, data2):
    """Compute the Kuiper statistic to compare two samples

    Warning: the fpp is quite approximate, especially for small samples.
    """
    data1, data2 = sort(data1), sort(data2)

    if len(data2)<len(data1):
        data1, data2 = data2, data1

    cdfv1 = searchsorted(data2, data1)/float(len(data2)) # this could be more efficient
    cdfv2 = searchsorted(data1, data2)/float(len(data1)) # this could be more efficient
    D = (amax(cdfv1-arange(len(data1))/float(len(data1))) + 
            amax(cdfv2-arange(len(data2))/float(len(data2))))

    Ne = len(data1)*len(data2)/float(len(data1)+len(data2))
    return D, kuiper_FPP(D, Ne)
