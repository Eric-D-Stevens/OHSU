"""Tests of the BitWeight Python wrapper."""

from __future__ import division

import unittest

from bitweight import BitWeight, BitWeightRangeError


class TestBitWeight(unittest.TestCase):

  def setUp(self):
    self.tiny = BitWeight(1, 1e6)
    self.half = BitWeight(.5)
    self.quarter = BitWeight(.25)
    self.eighth = BitWeight(.125)
    self.century = BitWeight(100)
    self.millenium = BitWeight(1000)

  def testNegativeAssertions(self):
    with self.assertRaises(BitWeightRangeError):
      unused_v = BitWeight(-.5)
    with self.assertRaises(BitWeightRangeError):
      unused_v = BitWeight(-1, 2)
    with self.assertRaises(BitWeightRangeError):
      unused_v = BitWeight(1, -2)
    with self.assertRaises(BitWeightRangeError):
      unused_v = BitWeight(1, 0)

  def testAddition(self):
    three_quarters = .75
    self.assertEqual((self.half + self.quarter).real(), .75)
    self.assertEqual((self.quarter + self.half).real(), .75)

    # test the code path for equal values
    self.assertEqual((self.quarter + self.quarter).real(), 0.5)

  def testMultiplication(self):
    one_quarter = .125
    self.assertEqual((self.half * self.quarter).real(), .125)
    self.assertEqual((self.quarter * self.half).real(), .125)

  def testDivision(self):
    self.assertEqual((self.half / self.quarter).real(), 2.)
    self.assertEqual((self.quarter / self.half).real(), .5)

  def testEquality(self):
    my_half = BitWeight(1, 2)
    self.assertEqual(self.half, my_half)
    self.assertEqual(self.half.real(), my_half.real())
    my_quarter = BitWeight(1, 4)
    self.assertEqual(self.quarter, my_quarter)
    self.assertEqual(self.quarter.real(), my_quarter.real())

  def testComparison(self):
    bws = [self.quarter, self.half, self.eighth]
    bws.sort()
    self.assertEqual([bw.real() for bw in bws], [.125, .25, .5])


if __name__ == "__main__":
  unittest.main()
