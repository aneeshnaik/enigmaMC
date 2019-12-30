#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 27 10:09:30 2019

@author: aneeshnaik
"""
import numpy as np


class Walker:
    def __init__(self, p0, k, lnprobfunc):
        """
        MCMC walker object.

        Parameters
        ----------
        p0 : array of ints, shape (26,)
            Initial mappings from encryption to decryption,
            e.g. array([0, 5, 1, 3, ...]) maps A->A, B->F, C->B, D->D, etc.
        k : int or float
            Attenuation length of exponential, or 'Jump size'
        lnprobfunc : function
            Function calculating log-probability associated with given mapping.
            Input should be array of ints, shape (26,), like p0 parameter.
            Output should be single float.

        Attributes
        ----------
        p0, k : -
            As in 'Parameters'
        p : Numpy array of ints, shape (26,)
            Current position of walker.
        lnprob : float
            Log-probability of current position of walker.
        bins : 1D numpy array
            Discrete 'bins' for sampling from proposal function,
            used in 'propose_nswaps'.
        """
        self.p0 = p0
        self.p = np.copy(self.p0)
        self.lnprobfunc = lnprobfunc
        self.lnprob = self.lnprobfunc(self.p)
        self.k = k
        self.bins = self.cumproposal(np.arange(-1, 40*self.k))
        return

    def proposal(self, n):
        """
        Exponential proposal function for number of mapping swaps.

        Parameters
        ----------
        n : int or array of ints, shape (N,)
            Number (or numbers if array) of swaps.

        Returns
        -------
        prob : float or array of floats, shape (N,)
            Probability (or probabilities if array) of given number of swaps.
        """
        prob = np.exp(-n/self.k)*(1-np.exp(-1/self.k))
        return prob

    def cumproposal(self, n):
        """
        CDF of exponential proposal function for number of mapping swaps.

        Parameters
        ----------
        n : int or array of ints, shape (N,)
            Number (or numbers if array) of swaps.

        Returns
        -------
        cdf : float or array of floats, shape (N,)
            Cumulative probability (or probabilities if array) of given n.
        """
        cdf = 1 - np.exp(-(n+1)/self.k)
        return cdf

    def propose_nswaps(self):
        """
        Propose a number of mapping swaps, drawn from exponential proposal
        function.

        Returns
        -------
        n_swaps : int
            Number of mapping swaps
        """
        x = np.random.sample()
        n_swaps = np.digitize(x, bins=self.bins) - 1
        return n_swaps

    def iterate(self):
        """
        Perform one Monte Carlo iteration.
        """

        # propose number of mapping swaps from exponential function
        n_swaps = self.propose_nswaps()

        # perform mapping swaps
        p_new = np.copy(self.p)
        for i in range(n_swaps):
            inds = np.random.choice(26, size=2, replace=False)
            p_new[inds] = p_new[np.flip(inds, axis=0)]

        # decide whether to accept new mapping
        lnprob_new = self.lnprobfunc(p_new)
        alpha = np.exp(lnprob_new - self.lnprob)
        u = np.random.sample()
        if u <= alpha:
            self.p = p_new
            self.lnprob = lnprob_new

        return
