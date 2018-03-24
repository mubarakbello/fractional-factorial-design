#-----------------------------------------------
#intdet.py - compute integer determinants
#Copyright (c) 2009, Imri Goldberg
#All rights reserved.
#
#Redistribution and use in source and binary forms,
#with or without modification, are permitted provided
#that the following conditions are met:
#
#    * Redistributions of source code must retain the
#		above copyright notice, this list of conditions
#		and the following disclaimer.
#    * Redistributions in binary form must reproduce the
#		above copyright notice, this list of conditions
#		and the following disclaimer in the documentation
#		and/or other materials provided with the distribution.
#    * Neither the name of the algorithm.co.il nor the names of
#		its contributors may be used to endorse or promote products
#		derived from this software without specific prior written permission.
#
#THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
#IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
#ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
#LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
#DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
#SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
#CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
#OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#-----------------------------------------------
import time
import gc

import numpy
from fractions import Fraction

def gcd(a,b):
    prev = a
    r = b
    while r != 0:
        prev,r = r, prev%r
    return prev

class Rational(object):
    def __init__(self, numerator, denominator=1, do_gcd = True):
        if isinstance(numerator, Rational):
            self.numerator = numerator.numerator
            self.denominator = numerator.denominator
            return
        self.numerator = numerator
        self.denominator = denominator
        assert isinstance(self.numerator, (int, int)), str(type(self.numerator))
        assert isinstance(self.denominator, (int, int)), str(type(self.denominator))
        if denominator<0:
            self.denominator = -denominator
            self.numerator = -numerator
        if do_gcd:
            g = gcd(self.numerator, self.denominator)
            self.numerator /= g
            self.denominator /= g
    def __repr__(self):
        if self.denominator == 1:
            return '%d' % self.numerator
        return '%d/%d' % (self.numerator, self.denominator)
    def inv(self):
        return Rational(self.denominator, self.numerator, False)
    def __add__(self, other):
        other = Rational(other)
        new_nom = self.numerator*other.denominator + other.numerator*self.denominator
        new_denominator = self.denominator*other.denominator
        return Rational(new_nom, new_denominator)
    def __neg__(self):
        return Rational(-self.numerator, self.denominator, False)
    def __sub__(self, other):
        return self + (-other)
    def __mul__(self, other):
        other = Rational(other)
        new_nom = self.numerator*other.numerator
        new_denominator = self.denominator*other.denominator
        return Rational(new_nom, new_denominator)
    def __div__(self, other):
        return Rational(self.numerator*other.denominator, self.denominator*other.numerator)
    def __radd__(self, other):
        return self+other
    def __rsub__(self, other):
        return other + (-self)
    def __rmul__(self, other):
        return self*other
    def __rdiv__(self, other):
        return self.inv()*other
    def __abs__(self):
        return abs(self.numerator)/float(abs(self.denominator))
    def __float__(self):
        return self.numerator/float(self.denominator)



def minor(a, i, j):
    no_col = numpy.hstack((a[:,:i], a[:,i+1:]))
    no_row = numpy.vstack((no_col[:j], no_col[j+1:]))
    return no_row

def first_row_minor(a, col):
    a = a[1:]
    no_col = numpy.hstack((a[:,:col], a[:,col+1:]))
    return no_col


def slowdet(a):
    assert len(a.shape) == 2
    assert a.shape[0] == a.shape[1]
    return _slowdet(a)

def _slowdet(a):
    sign = 1
    result = 0
    if a.shape[0] == 1:
        return a[0][0]
    for i in range(a.shape[0]):
        subdet = _slowdet(first_row_minor(a, i))
        result += a[0][i]*subdet*sign
        sign = -1*sign
    return result

def swaprows(m, i, j):
    if len(m.shape) == 1:
        m[i],m[j] = m[j].m[i]
    else:
        temp = m[i].copy()
        m[i] = m[j]
        m[j] = temp

class Timer(object):
    def __init__(self):
        self.start_time = time.time()
    def estimate(self, iter, max_iter):
        cur_time = time.time()
        elapsed = cur_time - self.start_time
        remaining = (elapsed/iter)*(max_iter-iter)
        print(iter, max_iter)
        print('elapsed: %.2f remaining: %.2f' % (elapsed, remaining))

def gauss_det(m):
    m = numpy.array([[Fraction(int(x)) for x in row] for row in m])
    h,w = m.shape
    assert h==w
    timer = Timer()
    subs = 0
    for i in range(h):
        if i%3 == 1:
            timer.estimate(i, h)
        first = True
        for j in range(i+1, h):
            x = m[j][i]
            if first:
                first = False
                cur_min = x.denominator, x.numerator
                cur_min_idx = j
            if (x.numerator, x.denominator) < cur_min:
                cur_min_idx = j
                cur_min = x
        if i != cur_min_idx:
            swaprows(m, i, cur_min_idx)
            subs += 1


        temp_row = m[i]/m[i][i]
        for j in range(i+1, h):
            m[j][i:] -= temp_row[i:]*m[j][i]
    #print(m)
    #return m
    return m.diagonal().prod()


def _gauss_det(m, eps = 1.0/(10**10)):
    m = numpy.array([[Fraction(int(x)) for x in row] for row in m])
    subs = 0
    (h, w) = (len(m), len(m[0]))
    for y in range(0,h):
        maxrow = y
        for y2 in range(y+1, h):    # Find max pivot
            if abs(m[y2][y]) > abs(m[maxrow][y]):
                maxrow = y2
        swaprows(m, y, maxrow)
        subs += 1
        if abs(m[y][y]) <= eps:     # Singular?
            return None
        for y2 in range(y+1, h):    # Eliminate column y
            c = m[y2][y] / m[y][y]
            m[y2][y:w] -= m[y][y:w]*c
    prod = m.diagonal().prod()
    if subs%2:
        return prod
    return -prod

mats = [[5,0,0,-1,8], [0,5,0,6,9], [2,0,5,0,0], [-8,3,0,5,0], [0,-4,0,0,5]]
print(_gauss_det(mats))