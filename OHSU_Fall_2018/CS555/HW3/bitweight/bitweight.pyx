"""BitWeight Python wrapper."""

from __future__ import division

cimport cbitweight as bw
from cython.operator cimport dereference as deref


class BitWeightRangeError(ValueError):

  pass


cdef class BitWeight(object):

  cdef bw.BitWeight *ptr

  def __init__(self, double n, double d=1.):
    # These assertions have to be repeated as Cython ignores C++ assertions.
    if n < 0.:
      raise BitWeightRangeError(n)
    if d <= 0.:
      raise BitWeightRangeError(d)
    self.ptr = new bw.BitWeight(n) if d == 1. else new bw.BitWeight(n, d)

  def __dealloc__(self):
    del self.ptr

  def real(self):
    return self.ptr.real()

  def log(self):
    return self.ptr.log()

  # Overloads.

  def __iadd__(self, BitWeight rhs):
    self.ptr.iadd(deref(rhs.ptr))
    return self

  def __imul__(self, BitWeight rhs):
    self.ptr.imul(deref(rhs.ptr))
    return self

  def __itruediv__(self, BitWeight rhs):
    self.ptr.idiv(deref(rhs.ptr))
    return self

  def __add__(BitWeight lhs, BitWeight rhs):
    cdef BitWeight result = BitWeight.__new__(BitWeight)
    result.ptr = new bw.BitWeight(deref(lhs.ptr) + deref(rhs.ptr))
    return result

  def __mul__(BitWeight lhs, BitWeight rhs):
    cdef BitWeight result = BitWeight.__new__(BitWeight)
    result.ptr = new bw.BitWeight(deref(lhs.ptr) * deref(rhs.ptr))
    return result

  def __truediv__(BitWeight lhs, BitWeight rhs):
    cdef BitWeight result = BitWeight.__new__(BitWeight)
    result.ptr = new bw.BitWeight(deref(lhs.ptr) / deref(rhs.ptr))
    return result

  def __richcmp__(BitWeight lhs, BitWeight rhs, int op):
    if op == 0:
      return deref(lhs.ptr) < deref(rhs.ptr)
    elif op == 2:
      return deref(lhs.ptr) == deref(rhs.ptr)
    elif op == 3:
      return not deref(lhs.ptr) == deref(rhs.ptr)
    raise NotImplemented("Operator {} not implemented.".format(op))
