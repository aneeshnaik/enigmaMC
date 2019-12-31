#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 31 16:36:43 2019

@author: aneeshnaik
"""
from constants import alphabet
import numpy as np


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
