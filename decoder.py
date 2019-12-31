#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 15:17:44 2019

@author: aneeshnaik
"""
from walker import Walker
from text_utils import clean, cleantext_to_matrix
from quadscore import QuadScore
import numpy as np


class Decoder:
    def __init__(self, ciphertext):
        """
        Main object that runs the MCMC algorithm. Primary function is the run()
        function.

        Parameters
        ----------
        ciphertext : str
            A single string containing the whole ciphertext

        Attributes
        ----------
        ct_orig : str
            The original ciphertext, as in parameters.
        ct_clean : str
            The original ciphertext, but all-caps and non-alphabet characters
            removed.
        ct_matrix : numpy array, shape (26, len(ct_clean))
            The cleaned ciphertext (ct_clean), recasted into a numpy array.
            Each column of the array represents a character of the ciphertext
            as a 26-element vector of boolean 0s, with a 1 indicating the
            character.

        Functions
        ---------
        lnprob :
            Calculate the log-probability associated with a given mapping.
        run :
            Run the MCMC.
        """
        self.ct_orig = ciphertext
        self.ct_clean = clean(ciphertext)
        self.ct_matrix = cleantext_to_matrix(self.ct_clean)

        self._qs = QuadScore()

        return

    def lnprob(self, theta):
        lnp = self._qs.lnprob(np.matmul(theta, self.ct_matrix))
        return lnp

    def initial_mapping():

        return

    def run(self, niter=50000):

        self.p0 = np.identity(26, dtype=bool)
        self.chain = np.zeros((niter+1, 26, 26), dtype=bool)
        self.probchain = np.zeros((niter+1))
        self.chain[0] = self.p0
        self.probchain[0] = self.lnprob(self.p0)
        w1 = Walker(p0=self.p0, k=30, lnprobfunc=self.lnprob)

        for i in range(niter):
            w1.iterate()
            self.chain[i+1] = w1.p
            self.probchain[i+1] = w1.lnprob
        return
