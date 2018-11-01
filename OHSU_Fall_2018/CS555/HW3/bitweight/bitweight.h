#ifndef _BITWEIGHT_H_
#define _BITWEIGHT_H_

#include <cassert>
#include <cmath>
#include <limits>

/* A "bitweight" is a positive floating-point number stored internally in
 * log-space as the negative base-two log of the real-space number. Addition,
 * multiplication, and division are overloaded; all other operators are left
 * undefined. Following the suggestion of Stroustrup (2014: 536f.), we define
 * the compound assignment operators in-class, then use these to create
 * definitions of the simple binary operators out-of-class. */

namespace bitweight {

template <typename T>
class BitWeightTpl {
 public:
  // Constructs BitWeightTpl from real-valued floating-point number type T;
  // it is set to infinity when the input value is zero.
  explicit BitWeightTpl<T>(const T x)
      : bw_(x == 0. ? std::numeric_limits<T>::infinity() : -log2(x)) {
    assert(x >= 0.);
  }

  // Constructs BitWeightTpl from fraction, by constructing the numerator, then
  // "dividing" by the denominator in place.
  BitWeightTpl<T>(const T n, const T d) : BitWeightTpl<T>(n) {
    *this /= BitWeightTpl<T>(d);
  }

  // Default constructors are all implicitly present, too.

  // Converts BitWeightTpl to real-valued number.
  T real() const { return exp2(-bw_); }
  
  // return the BW's negative log value
  T log() const { return bw_; }

  bool operator<(BitWeightTpl<T> rhs) { return bw_ > rhs.bw_; }

  bool operator==(BitWeightTpl<T> rhs) { return bw_ == rhs.bw_; }

  // The addition algorithm is a straightforward optimization of eq. 9.21 of
  // Manning & Schütze (2001). It defines "big" in terms of the size of T in
  // bits.
  static constexpr T big = 8 * sizeof(T) - 1;
  BitWeightTpl<T> &operator+=(BitWeightTpl<T> rhs) {
    // When the two terms are very close, we set the sum to the larger term.
    T diff = bw_ - rhs.bw_;
    if (diff > big) {
      bw_ = rhs.bw_;
      return *this;
    } else if (-diff > big) {
      return *this;  // Do nothing.
    }
    // Otherwise, we exponentiate the smaller term.
    if (diff > 0.) {
      bw_ -= log2(exp2(bw_ - rhs.bw_) + 1.);
    } else if (diff < 0.) {
      bw_ = rhs.bw_ - log2(1. + exp2(rhs.bw_ - bw_));
    } else {  // bw_ == rhs.bw_
      bw_ -= 1.;
    }
    return *this;
  }

  BitWeightTpl<T> &operator*=(BitWeightTpl<T> rhs) {
    bw_ += rhs.bw_;
    return *this;
  }

  BitWeightTpl<T> &operator/=(BitWeightTpl<T> rhs) {
    bw_ -= rhs.bw_;
    return *this;
  }

 private:
  T bw_;
};

template <typename T>
BitWeightTpl<T> operator+(BitWeightTpl<T> lhs, BitWeightTpl<T> rhs) {
  return lhs += rhs;
}

template <typename T>
BitWeightTpl<T> operator*(BitWeightTpl<T> lhs, BitWeightTpl<T> rhs) {
  return lhs *= rhs;
}

template <typename T>
BitWeightTpl<T> operator/(BitWeightTpl<T> lhs, BitWeightTpl<T> rhs) {
  return lhs /= rhs;
}

using BitWeight = BitWeightTpl<double>;

};  // namespace bitweight

#endif  // _BITWEIGHT_H_
