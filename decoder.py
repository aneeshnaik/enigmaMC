#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 21:32:54 2019

@author: aneeshnaik
"""

f = open("text_original.txt", 'r')
text_enc = f.readline()
f.close()
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
            'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']


def check_cipher(cipher):
    """
    Check that values in cipher are all lowercase alphabets, and no values are
    repeated (i.e. check one-to-one not many-to-one)
    """
    vals = []
    for val in cipher.values():
        if val is not None:
            assert val in alphabet, "Unrecognised value: "+val
            assert val not in vals, "Repeated value in cipher: "+val
            vals.append(val)

    return


def decrypt(code, cipher):
    """
    Given cipher (dict), decrypt code (str) and spit out decoded text (str)
    """

    decoded = ""
    for char in code:
        if char in alphabet:
            val = cipher[char]
            if val is None:
                decoded += '*'
            else:
                decoded += val
        elif char.swapcase() in alphabet:
            val = cipher[char.swapcase()]
            if val is None:
                decoded += '*'
            else:
                decoded += val.swapcase()
        else:
            decoded += char

    return decoded


def freq_analysis(code):
    frequencies = {x: 0 for x in alphabet}
    for char in code:
        if char in alphabet:
            frequencies[char] += 1
        elif char.swapcase in alphabet:
            frequencies[char.swapcase] += 1
    return frequencies


# key: val represents encrypted char: decrypted char
cipher = {'a': None,
          'b': 'a',
          'c': None,
          'd': None,
          'e': None,
          'f': None,
          'g': 'n',
          'h': None,
          'i': None,
          'j': None,
          'k': None,
          'l': None,
          'm': None,
          'n': None,
          'o': None,
          'p': 'e',
          'q': None,
          'r': None,
          's': None,
          't': 'o',
          'u': 't',
          'v': 's',
          'w': None,
          'x': None,
          'y': None,
          'z': None,
          }


freqs = freq_analysis(code)
print(sorted(freqs, key=freqs.get, reverse=True))
check_cipher(cipher)
text_dec = decrypt(text_enc, cipher)
print(text_dec)
