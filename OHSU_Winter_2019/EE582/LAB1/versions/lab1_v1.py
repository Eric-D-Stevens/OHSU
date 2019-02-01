''' docstring here '''

from scipy.io import wavfile
import numpy as np
import matplotlib.pyplot as plt


def plot_array(array):
    plt.plot(array)
    plt.show()

def plot_arrays(a1, a2):
    plt.plot(a1)
    plt.plot(a2)
    plt.show()

def load_wav(filename):
    ''' returns np arry of wave amplitude values '''
    _, data = wavfile.read(filename)
    return data



def convolve(input1, input2):
    ''' convolution function '''
    array_length = len(input1)
    output = np.zeros(2*array_length-1)
    assert len(input1) == len(input2)

    zeros = np.zeros(array_length)
    in_2_reverse = np.concatenate((zeros, np.flip(input2), zeros))

    for i in range(0, 2*array_length-1):
        output[i] = np.matmul(input1, in_2_reverse[-array_length-i-1:-i-1])

    return output


def correlate(input1, input2):
    ''' correlation function: auto_cor '''
    array_length = len(input1)
    output = np.zeros(2*array_length-1)
    assert len(input1) == len(input2)

    zeros = np.zeros(array_length)
    in_2_padded = np.concatenate((zeros, input2, zeros))

    for i in range(0, 2*array_length-1):
        output[i] = np.matmul(input1, in_2_padded[-array_length-i-1:-i-1])

    max_correlation = 0.0
    index = 0
    for i in range(len(output)):
        if output[i] > max_correlation:
            max_correlation = output[i]
            index = i
    index = index-array_length + 1
    return output, index

