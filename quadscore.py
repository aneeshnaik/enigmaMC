#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 10:18:55 2019

@author: aneeshnaik
"""
import numpy as np


class QuadScore:
    def __init__(self):
        """
        Object to read and store quadgram probability distribution, quickly
        outputs probabilities for any given text via 'lnprob' function.
        """

        # read file
        f = open('english_quadgrams.txt', 'r')
        self.qdict = {}
        for line in f:
            key, count = line.split()
            self.qdict[key] = int(count)

        # store lnprobs for all quadgrams in training set
        N = sum(iter(self.qdict.values()))
        for key, val in self.qdict.items():
            self.qdict[key] = np.log(val/N)

        # floor probability; given for quadgrams absent in training set
        self.floor = np.log(0.001/N)
        return

    def qsplit(self, text):
        """
        Split text into quadgrams.
        """
        qlist = []
        for i in range(len(text)-3):
            qlist.append(text[i:i+4])
        return qlist

    def lnprob(self, text):
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

        qlist = self.qsplit(text)
        lp = np.zeros(len(qlist))

        for i in range(len(qlist)):
            quad = qlist[i]
            if quad in self.qdict.keys():
                lp[i] = self.qdict[quad]
            else:
                lp[i] = self.floor

        return np.sum(lp)
