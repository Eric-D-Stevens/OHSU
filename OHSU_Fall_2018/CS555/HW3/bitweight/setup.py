from setuptools import setup, Extension
from Cython.Build import cythonize

setup(name="BitWeight",
      version="0.1",
      description="Underflow-proof floating-poing math for NLP",
      author="Kyle Gorman and Steven Bedrick",
      author_email="gormanky@ohsu.edu",
      install_requires=["Cython >= 0.22"],
      ext_modules=cythonize([Extension("bitweight", ["bitweight.pyx"],
                                       language="c++",
                                       extra_compile_args=["-std=c++11"])]),
      test_suite="bitweight_test",
)
