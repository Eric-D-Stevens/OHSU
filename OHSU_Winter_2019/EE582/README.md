# EE 580: Lab 1
### Eric D. Stevens
### January 31, 2019

## Overview

#### Python Version

* Python 2.7

#### Required Libraries
* NumPy
* SciPy
* MatPlotLib

#### Usage

Running the main program with `python lab1.py` will produce a 
demonstration of the function of all the sections in the lab.
Solutions to particular sections are implement in one or more
separate functions that can be viewed in the `lab1.py` file.


## Part 1

In this section a function to perform convolution is build from
scratch using the numpy library. The inputs, `input1` and 
`input2` are two numpy array like objects to be convolved with
each other. The return value of the function is another numpy
array that is the result of convolving the two input signals. 

This function sets variable `x_t` to the longer of the two inputs
and `h_t` to the shorter of the two inputs. From there an output
array of size `len(x_t) + len(h_t) - 1` is declared and initialized
with zeros. Another array then created by reversing `x_t` and then
placing zero arrays of size `len(h_t) - 1` on either end of it.
This array, named `x_reverse`, will be used to calculate the sum.
The convolution operation is done by sliding `h_t` across the 
`x_reversed` array and performing a matrix multiplication at each
step. The value of each matrix multiplication is set to the 
appropriate value in the output array. 

```python
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
```

## Part 2

In this section the convolution function is used to convolve
the provided sound file with the provided impulse responses. This
allows the user to move the signal around the room. Since we know
that there are 5 signals and we know that they are coming from 5
provided directions we can perform these convolution operations 
and then output the resulting sound file and listen to determine 
from which of the predetermined direction each file is coming from.

The first step in accomplishing this is to get the ability to 
move the signal around the room based on the provided files. The
function `move_signal()` accomplishes this task. The inputs to the
function are the input signal file path, the file paths for each
of the impulse response files, and the name of the desired output
file path. 

The function first loads the input files and ensures that the two
resulting impulse response arrays are the same length. Then each
impulse response is convolved with the input signal array to 
create the new output channel arrays `left_output` and 
`right_output`. These arrays will use the `float32` data format 
to allow the writing of the wav file and therefore need to be
normalized to a range of [-1,1]. This is done by dividing both
arrays by the maximum value in either of them. After this is
accomplished the file is written to a file path specified in
parameter list. 


```python
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
```

Next a function will be created to perform the above operation 
with every pair of provided impulse responses. This function
will also output a single audio file of all 5 outputs 
concatenated together to in order to test our ideas about the
direction the signal is coming from. 

This function `all_files()` has an input parameter `order_list`
that is a regular python list with the values in the list being
the order in which the user desires to process the impulse 
responses. If no value is provided, the function will output the
files 1-5 in numerical order. In other words, if we run the 
command `all_files([2,5,4,1,3])` we will get 6 output .wav files.
There will be .wav files for each of the response pairs, and a
.wav file that is the concatenation of these files in the 
order: 2, 5, 4, 1, 3. This concatenated file allows us to do
a final check to make sure the sound is sweeping around the
space and ensures we have the correct angles. All of these
files will end up in a subdirectory called `./output_wav_files/`.

```python
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
```

From listening to the output files of this function we can 
match each file to its corresponding output location.


| **Pair** | **Location** |
|----------|--------------|
| 1        | +80&deg;     |
| 2        | 0&deg;       |
| 3        | -40&deg;     |
| 4        | -80&deg;     |
| 5        | +40&deg;     |


## Part 3

In this section, the convolution function built in part one
will be altered slightly to create a correlation function.
This simply involves not reversing the `x_t` variable before
performing the sliding and summing operation. To notice the
difference, look at the code below and see that what was 
called `x_reverse` in the convolution function is now called
`x_padded` and does not have the reverse function involved.

Unlike the convolution function, the correlation function
returns two values. The first, `output`, is the np array
that resulted from the correlation operation. The second,
`index` is the index at which the correlation value was
maximum. 

It is important to note that the indices of the array do
not properly correspond with the indices of a properly 
performed correlation function. This is because correlation,
even with causal signals, will have values at negative 
indices. The requirements of this assignment do not 
necessarily need to keep track of these indices.

```python
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
```

## Part 4

The purpose of this section is to show that the auto-correlation
of Golay sequence pairs sum to zero and to explain how this fact
can be useful in the effort to reduce noise in signals.

To demonstrate the auto-correlation sum property of Golay sequence
pairs, a Golay sequence generator is built.

```python
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
```

Now we can use this function and the `correlate()` function to 
demonstrate the property as follows:

```python
>>> for i in range(1,4):
...     a,b = lab1.create_golay(i)
...     a_auto,_ = lab1.correlate(a,a)
...     b_auto,_ = lab1.correlate(b,b)
...     print '\n'
...     print 'a      ', a
...     print 'b      ', b
...     print 'a auto ', a_auto
...     print 'b auto ', b_auto
...     print 'a + b  ', a_auto+b_auto
... 


a       [1 1]
b       [ 1 -1]
a auto  [1. 2. 1.]
b auto  [-1.  2. -1.]
a + b   [0. 4. 0.]


a       [ 1  1  1 -1]
b       [ 1  1 -1  1]
a auto  [-1.  0.  1.  4.  1.  0. -1.]
b auto  [ 1.  0. -1.  4. -1.  0.  1.]
a + b   [0. 0. 0. 8. 0. 0. 0.]


a       [ 1  1  1 -1  1  1 -1  1]
b       [ 1  1  1 -1 -1 -1  1 -1]
a auto  [ 1.  0.  1.  0.  3.  0. -1.  8. -1.  0.  3.  0.  1.  0.  1.]
b auto  [-1.  0. -1.  0. -3.  0.  1.  8.  1.  0. -3.  0. -1.  0. -1.]
a + b   [ 0.  0.  0.  0.  0.  0.  0. 16.  0.  0.  0.  0.  0.  0.  0.]
```

As can be seen above, all of the auto-correlation sums have
only 0 coefficients at every point other than the origin. 
At the origin there is an coefficient value of 2(2^n).

The reason that Golay sequences are useful is that the fact 
that the autocorrelations sum to what is essentially an impulse
allows for a similar signal coming through a convolution 
operation, however, the negative and positive components
on either side of the zero mark prevent the amplification
of noise by canceling out the frequencies that are evenly
distributed.

## Part 5

In this section an effort is made to determine which of the 
provided impulse responses matches a mystery version impulse
response. The mystery response is one of the original files
with white noise layered on top of it.  

One method to determine which impulse response was the 
base for the mystery file is to run the correlation 
operation on the mystery file against all the original
impulse response files and then find the maximum
value of all of them. This is done with the function
`mystery_correlations()`, which will return a list
of tuples containing a label and a maximum value from
that labels correlation with the mystery file. 

```python
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
```

The function above can be used to get the solution as follows:

```python
>>> correlation_list = lab1.mystery_correlations()
>>> 
>>> for item in correlation_list: print item
... 
(73.0, 'Left 1')
(73.0, 'Right 1')
(76.0, 'Left 2')
(70.0, 'Right 2')
(78.0, 'Left 3')
(71.0, 'Right 3')
(79.0, 'Left 4')
(76.0, 'Right 4')
(70.0, 'Left 5')
(70.0, 'Right 5')
>>> 
>>> max(correlation_list)
(79.0, 'Left 4')
>>> 

```

The output above implies that the the signal in the mystery
response is the Left 4 impulse response with noise on top
of it. 


