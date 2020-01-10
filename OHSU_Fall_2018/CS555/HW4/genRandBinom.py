import numpy as np
import pdb 

L = 20 # length of sequences
t1=0.2
t2=0.5
t3=0.8
N1=50
N2=80
N3=120
Mat=np.zeros((N1+N2+N3,L))
for i in range(N1):
    Mat[i]=np.random.binomial(1,t1,L)
for i in range(N2):
    Mat[i+N1]=np.random.binomial(1,t2,L)
for i in range(N3):
    Mat[i+N1+N2]=np.random.binomial(1,t3,L)

np.random.shuffle(Mat)
np.savetxt('seq_H_T.txt',Mat.astype(int), fmt='%i')
