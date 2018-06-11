#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 20 11:54:58 2018

@author: Tony
"""

from math import sqrt, log, e
from scipy.stats import norm


class BSOption:
    def __init__(self, isCall, s, k, t, r, vol, div=0):
        # type: (object, object, object, object, object, object, object) -> object
        self.isCall = isCall
        self.s = s
        self.k = k
        self.t = t
        self.r = r
        self.vol = vol
        self.div = div

    def d1(self):
        return (log(self.s / self.k) + (self.r - self.div + (self.vol ** 2) / 2) * self.t) / (self.vol * sqrt(self.t))

    def d2(self):
        return self.d1() - self.vol * sqrt(self.t)

    def get_price(self):
        if self.isCall:
            return self.s * e**(-self.div*self.t) * norm.cdf(self.d1()) - self.k * e ** (-self.r * sqrt(self.t)) * norm.cdf(
                self.d2())
        else:
            return -self.s * e**(-self.div*self.t) * norm.cdf(-self.d1()) + self.k * e ** (-self.r * sqrt(self.t)) * norm.cdf(
                -self.d2())

    def get_delta(self):
        if self.isCall:
            return e**(-self.div*self.t) * norm.cdf(self.d1())
        else:
            return -e**(-self.div*self.t) * norm.cdf(-self.d1())

    def get_gamma(self):
        return e**(-self.div*self.t) * norm.pdf(self.d1()) / (self.s * self.vol * sqrt(self.t))

    def get_vega(self):
        return self.s * e**(-self.div*self.t) * norm.pdf(self.d1()) * sqrt(self.t)

    def get_theta(self):
        if self.isCall:
            return -self.s * e**(-self.div*self.t) * norm.pdf(self.d1()) * self.vol / (2 * sqrt(self.t)) - self.r * self.k * e ** (
                        -self.r * sqrt(self.t)) * norm.cdf(self.d2()) + self.div*self.s*e**(-self.div*self.t) * norm.cdf(self.d1())
        else:
            return -self.s * norm.pdf(self.d1()) * self.vol / (2 * sqrt(self.t)) + self.r * self.k * e ** (
                        -self.r * sqrt(self.t)) * norm.cdf(-self.d2()) - self.div*self.s*e**(-self.div*self.t) * norm.cdf(-self.d1())

    def get_rho(self):
        if self.isCall:
            return self.k * self.t * e ** (-self.r * sqrt(self.t)) * norm.cdf(self.d2())
        else:
            return -self.k * self.t * e ** (-self.r * sqrt(self.t)) * norm.cdf(-self.d2())

    def get_vanna(self):
        return -e**(self.div*self.t) * self.d2() / self.vol * norm.pdf(self.d1())

    def get_charm(self):
        if self.isCall:
            return -e**(-self.div*self.t) * (norm.pdf(self.d1())*((self.r-self.div)/(self.vol*sqrt(self.t)-self.d2()/(2*self.t))) + self.div*norm.cdf(self.d1()))
        else:
            return -e**(-self.div*self.t) * (norm.pdf(self.d1())*((self.r-self.div)/(self.vol*sqrt(self.t)-self.d2()/(2*self.t))) - self.div*norm.cdf(-self.d1()))

    def get_vomma(self):
        return self.get_vega()*self.d1()*self.d2()/self.vol

    def get_veta(self):
        return self.get_vega()*(self.div+(self.r-self.div)*self.d1()/(self.vol*sqrt(self.t))-(1+self.d1()*self.d2())/(2*self.t))

    def get_speed(self):
        return -self.get_gamma()/self.s*(self.d1()/(self.vol*sqrt(self.t)) + 1)

    def get_zomma(self):
        return self.get_gamma()*(self.d1()*self.d2()-1)/self.vol

    def get_color(self):
        return -self.get_gamma()/(2*self.t) * (2*self.div*self.t + 1 + (2*(self.r-self.div)*self.t - self.d2()*self.vol*self.vol)/(self.vol*sqrt(self.t))*self.d1())
# =============================================================================
# ## test
# aa = BSOption(1, 100, 110, 1.2, 0.02, 0.2, 0.1)
# print(aa.get_price())
# print(aa.get_delta())
# print(aa.get_gamma())
# print(aa.get_vega())
# print(aa.get_theta())
# print(aa.get_rho())
# =============================================================================
