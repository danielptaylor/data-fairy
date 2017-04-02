#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 19:52:42 2017

@author: daniel
"""


import importlib as imp
import random_data
imp.reload(random_data)
from random_data import random_d

data = random_d(nrows = 1000000, product_count = 10000)


df = data.transaction_df

flat = data.flat_file