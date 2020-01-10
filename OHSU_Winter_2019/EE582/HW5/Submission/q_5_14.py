
# coding: utf-8

# In[1]:


import numpy as np
import matplotlib.pyplot as plt

get_ipython().run_line_magic('matplotlib', 'inline')


# ## 5.14 a

# In[30]:


def quantize_signal(frequency=1./50., bits=4):
    
    # build axix for system
    axis = np.array((range(100)))
    
    # create sinwave from axis
    x_n = np.sin(axis*(2*np.pi*frequency))
    
    # number of quatizations is 2^bits
    bins = 2**bits
    
    # quantize sine wave into 'bins' bins
    xq_n = (np.floor(x_n*bins/2)+0.5)/(bins/2)
    
    # plotting
    plt.figure(figsize=(20,10))
    plt.plot(x_n)
    plt.step(axis,xq_n)
    plt.show()
    
    # calculation of total harmonic distortion
    THD = (np.sum(x_n**2) - np.sum(xq_n**2))/np.sum(x_n**2)
    
    # print the total harmonic distortion
    print("Total Harmonic Distortion: ", THD)
    
    return x_n, xq_n
    
    


# ## 5.14 b

# In[31]:


f_50_b_4 = quantize_signal(frequency=1./50., bits=4)


# In[32]:


f_50_b_6 = quantize_signal(frequency=1./50., bits=6)


# In[33]:


f_50_b_8 = quantize_signal(frequency=1./50., bits=8)


# In[34]:


f_50_b_16 = quantize_signal(frequency=1./50., bits=16)


# ## 5.14 c

# In[35]:


f_100_b_4 = quantize_signal(frequency=1./100., bits=4)


# In[36]:


f_100_b_6 = quantize_signal(frequency=1./100., bits=6)


# In[37]:


f_100_b_8 = quantize_signal(frequency=1./100., bits=8)


# In[38]:


f_100_b_16 = quantize_signal(frequency=1./100., bits=16)


# ## 5.14
# 
# In terms of the plots of the of the quantized signals, it is hard to tell the difference between the signals that are quantized into 8 bits and above. I believe this is because after four bit quantization, the time steps of the signal result in samples being taken at places that dont differ enough to notice the difference between 8 and 16 bits. However, in terms of the calculations of the total harmonic distortion, the higher the number of bits the lower the THD. This is because, although not visiable to the eye, the higher number of bits allows the quantized signal to more closely match the real sin wave.
# 
# The lower frequency signal seems to have a slightly lower harmonic distortion. This is likely because the slower motion of the signal allows for quantization with lower magnitude high frequency components. 
