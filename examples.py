#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 19:52:42 2017

@author: daniel
"""

from datafairy import DataFairy

data = DataFairy(nrows = 200000, product_count = 10000)

# Access transaction data like ...

trans = data.transaction_df

# Access product table like ...

product = data.product_df

# Access flat_file (i.e. transaction data combined with product information) like this

flat = data.flat_file