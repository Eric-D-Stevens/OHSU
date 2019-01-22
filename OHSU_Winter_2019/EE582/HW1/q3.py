''' Question 3 of CH 2 Homework '''

# a.

h = [0 for i in range(20)]
d = [0 for i in range(20)]
d[0] = 1.0

for n in range(10):
    h[n] = 0.5*d[n] + 0.5*d[n-3] + h[n-1]

print h


# b.

h = [0 for i in range(20)]
d = [0 for i in range(20)]
d[0] = 1.0

for n in range(10):
    h[n] = 0.5*d[n-2] + (1.0/3.0)*h[n-1] + (1.0/8.0)*h[n-2]

print h



# c.

h = [0 for i in range(20)]
d = [0 for i in range(20)]
z = [0 for i in range(20)]
d[0] = 1.0

for n in range(10):
    z[n] = d[n]+(2)*z[n-1]
    h[n] = z[n] + (3)*h[n-1]

print h



