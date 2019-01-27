#DSP: Lab 1
### Eric D. Stevens
### January 31, 2019

In this lab we analyze the sound

'''{python}
def convolve(input1, input2):

    ''' Perfroms convolution operation on two input np.array
    objects. Sets the smaller of the two inputs to 'h_t' and
    the longer of the two to x_t. Returns an np.array that is
    the convolution sum of the two signals. '''

    # set x_t to the longer signal and h_t to the shorter
    if len(input1) == len(input2):
        x_t = input1
        h_t = input2
    else:
        x_t = max(input1, input2, key=len)
        h_t = min(input1, input2, key=len)

    x_length = len(x_t)
    h_length = len(h_t)

    # empty output array to be filled
    output = np.zeros(x_length + h_length - 1)

    # reverse x_t and pad with zeros to prep for convolution
    x_reverse = np.concatenate((np.zeros(h_length),
                                np.flip(x_t),
                                np.zeros(h_length)))

    # convolution operation. loop shifts through
    for i in range(x_length+h_length-1):
        output[i] = np.matmul(h_t, x_reverse[-h_length-i-1:-i-1])

    # output is np.array object
    return output





'''
