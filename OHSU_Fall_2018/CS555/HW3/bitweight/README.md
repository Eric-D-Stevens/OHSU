# BitWeight

This C++ header and accompanying Python module provide classes designed to make it easier to work with log-probabilites in NLP and ML applications. 

A BitWeight is a real-space value represented internally as a negative base-2 logarithm, similar to that used in the log probability semiring, and used to avoid underflow. 

BitWeight is (c) 2014 by Kyle Gorman and Steven Bedrick, and is released under the 3-clause BSD License. See `LICENSE.txt` for more details.

# Install Instructions

Dependencies
* Cython >= 0.22
   
Clone the repository, enter the directory and run 

```
python setup.py install
```


