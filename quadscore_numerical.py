#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 10:18:55 2019

@author: aneeshnaik
"""
import numpy as np
from constants import alphabet


class QuadScore:
    def __init__(self):
        """
        Object to read and store quadgram probability distribution, quickly
        outputs probabilities for any given text via 'lnprob' function.
        """

        # read file, convert each quad into numerical tuple, e.g. 'ABCD' -> (0, 1, 2, 3)
        f = open('english_quadgrams.txt', 'r')
        self.qdict = {}
        for line in f:
            quad, count = line.split()
            c0 = alphabet.index(quad[0])
            c1 = alphabet.index(quad[1])
            c2 = alphabet.index(quad[2])
            c3 = alphabet.index(quad[3])
            key = (c0, c1, c2, c3)
            self.qdict[key] = int(count)

        # store lnprobs for all quadgrams in training set
        N = sum(iter(self.qdict.values()))
        for key, val in self.qdict.items():
            self.qdict[key] = np.log(val/N)

        # floor probability; given for quadgrams absent in training set
        floor = np.log(0.001/N)
        for i in range(26):
            for j in range(26):
                for k in range(26):
                    for l in range(26):
                        key = (i, j, k, l)
                        if key not in self.qdict.keys():
                            self.qdict[key] = floor
        return

    def qsplit(self, tmatrix):
        """
        Split text into quadgrams.
        """
        nquads = tmatrix.shape[1]-3
        q = [tuple(tmatrix[:, i:i+4].T.nonzero()[1]) for i in range(nquads)]
        return q

    def lnprob(self, tmatrix):
        """
        Based on stored probability distribution, give total ln-probability of
        list of quadgrams, i.e. sum of individual ln-probs.

        Parameters
        ----------
        qlist : list
            List of strings, each string consisting of 4 uppercase characters

        Returns
        -------
        lnprob : float
            Probability associated with quadgram.
        """

        qlist = self.qsplit(tmatrix)
        lp = np.zeros(len(qlist))

        for i in range(len(qlist)):
            quad = qlist[i]
            lp[i] = self.qdict[quad]

        return np.sum(lp)
