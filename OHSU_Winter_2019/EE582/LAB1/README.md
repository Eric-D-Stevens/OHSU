# DSP: Lab 1
### Eric D. Stevens
### January 31, 2019

In this lab we analyze the sound

## Part 1:

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
step. The value of each matrix mulitplication is set to the 
appropriate value in the output array. 

```python
def convolve(input1, input2):

    ''' Perfroms convolution operation on two input np.array
    objects. Sets the smaller of the two inputs to 'h_t' and
    the longer of the two to x_t. Returns an np.array that is
    the convolution sum of the two signals. '''
```

## Part 2:

In this section the convolution function is used to convolve the
the provided sound file with the provided impulse responses. This
allows the user to move the signal around the room. Since we know
that there are 5 signals and we know that they are coming from 5
provided directions we can perform these convolution operations 
and then output the resulting sound file and listen to determine 
from which of the predetermined direction each file is coming from.

The first step in accomplishing this is to get the abbility to 
move the signal around the room based on the provided files. The
function `move_signal()` acomplishes this task. The inputs to the
function are the input signal file path, the file paths for each
of the impulse response files, and the name of the desired output
file path. 

The function first loads the input files and ensures that the two
resulting impuse response arrays are the same lenght. Then each
impulse response is convolved with the input signal array to 
create the new output channel arrays `left_output` and 
`right_output`. These arrays will use the `float32` data format 
to allow the writing of the wav file and therefore need to be
normalized to a range of [-1,1]. This is done by dividing both
arrays by the maximum value in either of them. After this is
acomplished the file is written to a file path specified in
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
```

Next a function will be created to perform the above operation 
with every pair of provided impulse responses. This function
will also output a single audio file of all 5 outputs 
concatenated together to in order to test our ideas about the 
the direction the signal is coming from. 

This function `all_files()` has an input parameter `order_list`
that is a regular python list with the values in the list being
the order in which the user desires to process the impulse 
responses. If no value is provided, the function will output the
files 1-5 in numerical order. 
