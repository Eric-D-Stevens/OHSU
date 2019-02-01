''' docstring here '''

from scipy.io import wavfile
import numpy as np
import matplotlib.pyplot as plt
import os


def plot_array(array):
    ''' plot single array '''
    plt.plot(array)
    plt.show()

def plot_arrays(a_1, a_2):
    ''' ploat two arrays '''
    plt.plot(a_1)
    plt.plot(a_2)
    plt.show()

def load_wav(filename):
    ''' returns np arry of wave amplitude values '''
    _, data = wavfile.read(filename)
    return data


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


def correlate(input1, input2):

    ''' Correlation function does the exact same thing as the
    convolution function except that it does not flip the input
    signal. Also the return values include the output array as
    well as the shift index that resulted in the maximum score.'''

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

    # pad x_t to prep for correlation sum
    x_padded = np.concatenate((np.zeros(h_length),
                               x_t,
                               np.zeros(h_length)))

    # correlation sum
    for i in range(x_length+h_length-1):
        output[i] = np.matmul(h_t, x_padded[-h_length-i-1:-i-1])

    # get max correlation index
    max_correlation = 0.0
    index = 0
    for ind in range(len(output)):
        if output[ind] > max_correlation:
            max_correlation = output[ind]
            index = ind
    index = index - x_length + 1 # this is wrong, is -len on auto

    # output is np.array and index is the shift of highest allignment
    return output, index


def move_signal(input_signal_file='wav_files/sentence.wav',
                output_signal_file='output_sentence1.wav',
                left_impulse_response='wav_files/L1.wav',
                right_impulse_reponse='wav_files/R1.wav'):

    ''' This function will move the senteance file around the room.
    The inputs to the the function are file names. The input_signal_file
    is the sentence that should be moved around the room. The left and
    right impulse responses are the provided response files and the output
    file is the desired name of the file produced by the function.'''

    # load signal file and left and right impluse responses
    x_t = load_wav(input_signal_file)
    h_l_t = load_wav(left_impulse_response)
    h_r_t = load_wav(right_impulse_reponse)

    # impulse response must be same lenght for multichannel output
    assert len(h_l_t) == len(h_r_t)

    # convolve input signal with both impulse response
    left_output = convolve(x_t, h_l_t)
    right_output = convolve(x_t, h_r_t)

    ''' The convolution function results in very large number in the
    output. These outputs will not work as inputs to the wave file
    writing function. In order to comply with the scipy wave writeing
    function we convert all values to numpy data type float32 with a
    normalized range of [-1.0, 1.0]. '''

    # find the max value in either of the channel outputs
    max_l = max(np.abs(left_output))
    max_r = max(np.abs(right_output))
    maximum = max(max_l, max_r)

    # normalize the channels to a range [-1, 1]
    left_output /= maximum
    right_output /= maximum

    # convert to proper datatype for wave write
    left_output = left_output.astype('float32')
    right_output = right_output.astype('float32')
    output = np.array([left_output, right_output])

    # write file
    wavfile.write(output_signal_file, 44100, output.T)

    return output


def all_files(order_list=[1, 2, 3, 4, 5]):

    ''' runs the 'move_signal' functions on all
    input files and creates an ouptut file for each one.
    Also creates a single concatenated file of all input
    files in the order of the values in the parameter 'order_list'
    assumes that all input wave files are in a folder called
    'wav_files/' and that the left input response files are
    titled L1.wave, L2.wav, ... and the right are R1.wav
    R2.wave ... It also assumes there is an output directory
    called 'output_wav_files/' where the files will be
    written to. The input signal file must be file
    'wav_files/sentence1.wav'. addition: a file of '''

    # one long audio file in the order of parameter list
    all_files_output = np.empty([2, 0])

    # ensure output directory exits
    if not os.path.exists('./output_wav_files/'):
        os.makedirs('./output_wav_files/')

    # loop through each file
    for number in order_list:
        lir = 'wav_files/L'+str(number)+'.wav'
        rir = 'wav_files/R'+str(number)+'.wav'
        output_file = 'output_wav_files/output_sentence'+str(number)+'.wav'

        # write for current file
        file_out = move_signal(output_signal_file=output_file,
                               left_impulse_response=lir,
                               right_impulse_reponse=rir)

        # concat current file to long file
        all_files_output = np.append(all_files_output, file_out, axis=1)

    # write long file
    long_file_name = 'output_wav_files/file_concat.wav'
    wavfile.write(long_file_name, 44100, all_files_output.T)

def create_golay(n_order=1):
    ''' returns Golay sequence pair, each of size 2^n_order '''

    # inital golay sequence pair, order 1
    golay_pos = np.array([1, 1])
    golay_neg = np.array([1, -1])

    if n_order == 1:
        return (golay_pos, golay_neg)

    # itterative implementation of recursive generation
    for i in range(1,n_order):
        agolay = np.append(golay_pos, golay_neg)
        bgolay = np.append(golay_pos, -1*golay_neg)
        golay_pos = agolay
        golay_neg = bgolay

    return golay_pos, golay_neg


def mystery_correlations(make_plot=False):

    ''' This function runs the corrlation function
    on the mystery file agains all impulse response
    files. if the 'make_plot' variable is set to
    True then a plot of the correlations will be
    made. The return value is a list of tuples that
    contain the maximum value of corrlation result
    and a label the value that it corresponds to'''

    # holds max, label pair
    cor_list = []

    # load and normalize
    myst = load_wav('wav_files/new_mystery.wav')
    myst = myst/max(abs(myst))

    # loop through all impulse response files
    for i in range(1,6):

        # correlation for left right impulse responses, normalized
        impulse_l = load_wav('wav_files/L'+str(i)+'.wav')
        impulse_r = load_wav('wav_files/R'+str(i)+'.wav')
        impulse_l = impulse_l/max(abs(impulse_l))
        impulse_r = impulse_r/max(abs(impulse_r))
        cor_l, _ = correlate(myst, impulse_l)
        cor_r, _ = correlate(myst, impulse_r)

        # create plot
        if make_plot:
            plt.plot(cor_l, label='Left '+str(i))
            plt.plot(cor_r, label='Right '+str(i))

        # create and append max, label pair
        cor_list.append((np.amax(cor_l), 'Left '+str(i)))
        cor_list.append((np.amax(cor_r), 'Right '+str(i)))

    # plot
    if make_plot:
        plt.legend()
        plt.show()

    return cor_list


def main():
    '''this function can be ran to test demonstrate
    outputs for all the sections of the assignments'''

    print '\n\n'

    # PART 1: Convolution

    # shift signal with ofset delta
    signal = np.array([0,0,1,2,3,4,5,6,7,8,9,0,0,0,])
    delta_5 = np.array([0,0,0,0,0,1,0,0])
    convolved = convolve(signal,delta_5)

    print 'PART 1: Convolution\n'
    print 'Input Signal: ', signal
    print 'Impulse Response: ', delta_5
    print 'Convolution Result: ', convolved
    print '\n\n'


    # Part 2: Signal Localization

    # run progam on all files
    order_of_file_concatination = [4,3,2,5,1]
    all_files(order_list=order_of_file_concatination)

    print 'Part 2: Signal Localization\n'
    print 'All files saved to ./output_wav_files/'
    print 'File concatenation in order ', order_of_file_concatination
    print 'Concat file name: ./output_wav_files/file_concat.wav'
    print '\n\n'


    # Part 3: Correlation

    signal = np.array([1,1,1,0,0,0,0,0])
    correlated,_ = correlate(signal, signal)

    print 'Part 3: Correlation\n'
    print 'Input Signal: ', signal
    print 'Correlation Result: ', correlated
    print '\n\n'


    # Part 4: Golay Sequences

    n = 3
    print 'Part 4: Golay Sequences\n'
    print 'Generating Golay sequences from size 2 ^ 1 to  2 ^', n
    for i in range(1,n+1):
        print ' '
        a,b = create_golay(i)
        a_auto,_ = correlate(a,a)
        b_auto,_ = correlate(b,b)
        print 'a      ', a
        print 'b      ', b
        print 'a auto ', a_auto
        print 'b auto ', b_auto
        print 'a + b  ', a_auto+b_auto
    print '\n\n'


    # Part 5: Mystery File

    print 'Part 5: Mystery file Correlation\n'
    print 'getting max correlation values...'
    corelation_lable_pairs = mystery_correlations()
    for item in corelation_lable_pairs:
        print item
    print ''
    print 'Maximum Correlation: ', max(corelation_lable_pairs) 


if __name__ == "__main__":
    main()
