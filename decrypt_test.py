#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 27 13:12:48 2019

@author: aneeshnaik
"""
import numpy as np
from constants import alphabet


def clean(text):
    """
    Make text uppercase and remove spaces and special characters
    """
    ct_clean = text.upper()
    for char in ct_clean:
        if char not in alphabet:
            ct_clean = ct_clean.replace(char, '')
    return ct_clean


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


def matrix_to_cleantext(matrix):

    text = ""
    for col in range(matrix.shape[1]):
        char = alphabet[np.where(matrix[:, col])[0][0]]
        text += char
    return text


# =============================================================================
# text = "The quick brown fox jumped over the lazy dog."
# cleantext = clean(text)
# 
# a = cleantext_to_matrix(cleantext)
# 
# mapping = np.identity(26, dtype=bool)
# mapping[[0, 1]] = mapping[[1, 0]]
# 
# a = np.matmul(mapping, a)
# text_new = matrix_to_cleantext(a)
# print(text_new)
# 
# quads = [tuple(a[:, i:i+4].T.nonzero()[1]) for i in range(a.shape[1]-3)]
# 
# =============================================================================
#text = clean(text)