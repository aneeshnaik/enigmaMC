#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 15:17:44 2019

@author: aneeshnaik
"""
from walker import Walker
from quadscore_numerical import QuadScore
from constants import alphabet
import numpy as np
qs = QuadScore()


class Decoder:
    def __init__(self, ciphertext):

        self.ct_orig = ciphertext
        self.ct_clean = clean(ciphertext)
        self.ct_matrix = cleantext_to_matrix(self.ct_clean)

        return

    def lnprob(self, theta):
        lnp = qs.lnprob(np.matmul(theta, self.ct_matrix))
        return lnp

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


def clean(text):
    """
    Make text uppercase and remove spaces and special characters
    """
    ct_clean = text.upper()
    for char in ct_clean:
        if char not in alphabet:
            ct_clean = ct_clean.replace(char, '')
    return ct_clean


def decrypt(text, theta):
    for i in range(26):
        text = text.replace(alphabet[i], alphabet[theta[i]])
    return text


def cleantext_to_matrix(cleantext):
    """
    Convert cleaned (i.e. all caps, no spaces or non A-Z characters) text to
    matrix, shape (26, len(cleantext)).
    """
    matrix = np.zeros((26, len(cleantext)), dtype=bool)

    for i in range(len(cleantext)):
        char = cleantext[i]
        if char not in alphabet:
            assert False
        matrix[alphabet.index(char), i] = True

    return matrix

# load text
f = open("ciphertext.txt", 'r')
ct = f.readline()
f.close()

dec = Decoder(ct)
dec.run()
