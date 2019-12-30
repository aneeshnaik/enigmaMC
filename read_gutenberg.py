#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 26 13:54:20 2019

@author: aneeshnaik
"""
from constants import alphabet

filename = "gutenberg_samples/three_men_in_a_boat.txt"
f = open(filename, 'r')
ct = f.read()
f.close()
ct_clean = clean(ct)

