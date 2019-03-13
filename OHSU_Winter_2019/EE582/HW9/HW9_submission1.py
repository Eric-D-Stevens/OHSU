# Eric D. Stevens
# March 12, 2019
# Homework 9


import numpy as np
from scipy.signal import lfilter


def random_tf():
    """create random filter coefficients"""
    Nb = np.random.randint(1, 16)
    if Nb == 1:
        Na_min = 2  # so that we are testing _something_
    else:
        Na_min = 1
    Na = np.random.randint(Na_min, 16)

    def term(N):  # creation of filter coefficients via poles and zeros
        N2 = N // 2
        r = np.random.random(N2)
        w = np.random.random(N2) * np.pi
        z = r * np.exp(1j * w)
        p = np.r_[z, np.conjugate(z)]
        if N % 2:  # odd order
            p = np.r_[p, np.random.random_sample(1)]
        assert len(p) == N
        Q = np.poly(p)
        assert np.isreal(Q).all()
        return np.atleast_1d(Q)  # otherwise Q could be a scalar

    b = term(Nb)
    a = term(Na)
    return b, a




def tf2latc(b):
    M = len(b)
    K = np.zeros(M)
    K[0] = 1  # implicit
    b = b / b[0]
    b1 = np.empty_like(b)  # allocate memory for the new time-step
    for m in range(M - 1, 0, -1):
        b1[0] = 1
        K[m] = b[m]
        for k in range(1, m):
            b1[k] = (b[k] - b[m] * b[m-k]) / (1 - b[m] * b[m])
        b[:] = b1  # switch
    return K





def p1():
    """latc2tf implementation"""
    def latc2tf(K):
        """~10 lines"""

        M = len(K)
        b_past = np.zeros(M)
        b_past[0] = 1
        b_past[1] = K[1]

        for m in range(2,M):
            b_curr = np.zeros(M)
            b_curr[0] = 1
            b_curr[m] = K[m]
            for k in range(1,m):
                b_curr[k] = b_past[k]+b_curr[m]*b_past[m-k]
            b_past[:] = b_curr[:]
        return b_past


    for t in range(100):
        k = np.r_[1, np.random.random_sample(10)]  # any longer than this will result in significant numerical imprecision
        b = latc2tf(k)
        k2 = tf2latc(b)
        assert np.allclose(k, k2)



def p2():
    """lattice filter implementation"""
    def latcfilt(K, x):
        """~15 lines"""
        M = len(K)
        f = np.zeros(M)
        g = np.zeros(M)
        g_n_minus_1 = np.zeros(M)
        y = np.zeros(len(x))

        for i in range(len(x)):
            f[0] = x[i]
            g_n_minus_1[:] = g[:]
            g[0] = x[i]
            g_m = x[i]
            for m in range(1,M):
                f[m] = f[m-1] + K[m]*g_n_minus_1[m-1]
                g[m] = K[m]*f[m-1] + g_n_minus_1[m-1]
            y[i] = f[-1]
        return y

    # test
    for t in range(42):
        b, a = random_tf()
        x = np.random.random_sample(1000)

        k = tf2latc(b)
        y1 = latcfilt(k, x)
        y2 = lfilter(b, [1.], x)
        assert np.allclose(y1, y2)




def p3():
    """TDF2 filter implementation"""
    def tdf2(b, a, x):
        """~12 lines"""

        # make arrays same size
        N = max(len(a), len(b))
        bn = np.zeros(N)
        an = np.zeros(N)
        bn[:len(b)] = b[:]
        an[:len(a)] = a[:]

        # holds w values
        w = np.zeros(len(bn))

        # holds output
        y = np.zeros(len(x))

        # for each input value
        for i in range(len(x)):

            # set the output
            y[i] = x[i]*b[0]+w[1]

            # for each time delay
            for n in range(1,N-1):

                # cascade down calculations
                w[n] = w[n+1]+(x[i]*bn[n])-(y[i]*an[n])

            # set final w value
            w[-1] = (x[i]*bn[N-1])-(y[i]*an[N-1])

        return y

    # test
    for t in range(42):
        b, a = random_tf()
        x = np.random.random_sample(1000)

        y1 = tdf2(b, a, x)
        y2 = lfilter(b, a, x)

        assert np.allclose(y1, y2)




if __name__ == '__main__':
    p1()
    p2()
    p3()

