''' Eric D. Stevens : DSP : Chapter 7 Assignment '''

import numpy as np
from numpy.fft import fft, ifft, rfft, irfft


def p1():
    """roll-your-own DFT and IDFT"""
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

    def idft(X, N=None):
        """IDFT, 1 line"""
        return dft(X, N, inverse=True)


def p2():
    """create an A major chord via spectral synthesis, ~10 lines"""
    fs = 16000
    f1 = 440  # A4
    f2 = 554  # C#5
    f3 = 659  # E5

    '''*************************************************************************'''
    X = np.zeros(fs//2).astype('float32')
    X[f1] = 1
    X[f2] = 1
    X[f3] = 1
    x = irfft(X)
    x /= np.max(x)
    '''*************************************************************************'''

    from scipy.io import wavfile
    wavfile.write('chord_new.wav', fs, (x * 32000).astype(np.int16))


def p3():
    """overlap-add approach"""
    def overlap_add(x, h, L=128):
        """OLA, ~13 lines"""
        N = len(x)
        assert N % L == 0, 'len(x) must be a multiple of the block length'

        '''*************************************************************************'''
        windows = [np.convolve(x[i*L:(i+1)*L], h) for i in range(N//L)]
        y = np.zeros(N+len(h)-1)
        for i in range(len(windows)):
            y[i*L:(i+1)*L + len(h) - 1] += windows[i] 
        '''*************************************************************************'''

        return y

    L = 128  # block size
    x = np.random.randint(-128, 128, L * 8)
    h = np.random.randint(-128, 128, 42)
    y1 = np.convolve(x, h)
    y2 = overlap_add(x, h, L)
    assert np.allclose(y1, y2)


if __name__ == '__main__':
    p1()
    p2()
    p3()

