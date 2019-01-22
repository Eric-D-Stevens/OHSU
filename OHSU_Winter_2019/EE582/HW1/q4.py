''' This small scriptku calculates the zero state response
for a system described by x and y coefficents and an
input matix. The y coefficents are not needed to solve
this problem but they are declared here to demonstrate
the translation of the problem into code. The time shift
of the input signal is also not considered in the output
but one can simply interpret the output as shifted to the
appropriate place, in this example the first index of the
output can be interpreted ans n = -2.'''

# y(n) + (1/2)*y(n-1) 
y_coeffs = [1.0, 0.5, 0, 0, 0, 0, 0, 0, 0, 0]

# x(n) + 2*x(n-1)
x_coeffs = [1.0, 0, 2.0, 0, 0, 0, 0, 0, 0, 0]

# input signal ignoring negative time shift.
# interpret first index of output as n = -2.
x_inputs = [1.0, 2.0, 3.0, 4.0, 2.0, 1.0, 0, 0, 
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

def get_y_zs(x_cfs, x_ins):
    ''' embedded loop to calculate zero input response'''
    y_zs = [0 for n in range(10)]
    for n in range(10):
        for k in range(10):
            y_zs[n] += x_cfs[k]*x_ins[n-k]
    return y_zs

# Run the scirpts on the inputs
y_zs = get_y_zs(x_coeffs, x_inputs)
print y_zs
