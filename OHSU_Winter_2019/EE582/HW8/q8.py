'''
Instructions
Please implement the Radix-2 FFT algorithm, use the attached file as a template.

'''


import numpy as np

def dft(x, N=None, inverse=False):
    """DFT, ~6 lines"""
    L = len(x)
    if N is None:
        N = L

    '''*************************************************************************'''
    X = np.array([((1/float(N))**(inverse))*np.sum(x[:N]*np.exp(((-1)**(not inverse))*2j*np.pi*k*np.arange(L)[:N]/N))
                  for k in np.arange(N)])
    '''*************************************************************************'''

    return X

def fft(x, N=None, inverse=False):

    """FFT implementation, ~14 lines"""
    L = len(x)
    if N is None:
        N = L

    # in the case that len(x) > n
    if N<L:
        x = x[:N]
        L=N

    assert N % 2 == 0, 'N must be a power of 2'
    if N > 4:  # ad hoc threshold
        xn_evn = [x[i] for i in np.arange(L/2, dtype=int)*2]
        xn_odd = [x[i] for i in np.arange(L/2, dtype=int)*2+1]

        Xk_evn = fft(xn_evn, N=(N//2), inverse=inverse)# recursively calling ourselves
        out_exp = np.exp(np.arange((N/2))*((-1)**(not inverse))*2j*np.pi/N)
        Xk_odd = out_exp*fft(xn_odd, N=(N//2), inverse=inverse)# recursively calling ourselves

        Xk = np.zeros(N, dtype=np.complex128)
        for i in range(int(N/2)):
            Xk[i] = Xk_evn[i] + Xk_odd[i]
            Xk[i+int(N/2)] = Xk_evn[i] - Xk_odd[i]

        return ((1/2)**(inverse))*Xk

    else:
        return  dft(x, int(N), inverse=inverse)  # use either your solution, the official answer, or numpy's fft here


# Fast call to inverse Rad2 FFT
def ifft(X, N=None):
    return fft(X, N, inverse=True)


# Test script with bug fix and confirmation output
for N in [32,64,128]:

    x = np.random.randint(-128, 128, 64)
    X = fft(x, N)
    X_gold = np.fft.fft(x, N)

    assert np.allclose(X, X_gold)
    print('passed test fft: N = ', N, 'L = ', len(x))

    X = np.random.randint(-128, 128, 64)
    x = ifft(X, N)
    x_gold = np.fft.ifft(X, N)


    assert np.allclose(x, x_gold)
    print('passed test ifft: N = ', N, 'L = ', len(X))

