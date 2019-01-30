#DSP: Lab 1
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


