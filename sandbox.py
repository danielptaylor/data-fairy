#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 18:07:46 2017

@author: daniel
"""

import numpy as np
import random
import pandas as pd
from datetime import datetime
import radar # TODO: Add capability to radar to specify time of day and week weightings
import json

def getter(column, args):
    
    """
    Run the get function for the column in question
    """
    
    return get_list[column](args)


def get_product_id(args):
    
    return random.randint(0,len(product_dict.keys())-1)


def get_transaction_id(args):
    trans_per_customer = transactions_per_customer
    count = trans_per_customer * customer_count
    
    transaction_id = random.randint(1,count)
    
    return transaction_id


def get_customer_id(args):    
       
    try:        
        # Get existing customer_id for transaction if exists
        customer_id = trans_cust[args['transaction_id']]
    except KeyError:        
        customer_id = random.randint(1,customer_count)
        trans_cust[args['transaction_id']] = customer_id        
    
    return customer_id


def get_datetime(args):
    
    try:
        # Get existing datetime for transaction if exists        
        return trans_datetime[args['transaction_id']]
    except KeyError:        
        row_datetime =  radar.random_datetime(date_min, date_max)        
        trans_datetime[args['transaction_id']] = row_datetime
        return row_datetime
    
    
def get_quantity(args):
    
    return random.randint(quantity_range['min'],quantity_range['max'])


row_count = 100000

customer_count =  row_count / 5
transactions_per_customer =  5
quantity_range = {'min': 1, 'max': 3}
product_count = row_count / 1000

trans_dict = {}

trans_cust = {}
product_info = {}
trans_dict = {}
trans_datetime = {}


"""
Build product hierarchy
"""


columns = ['transaction_id','customer_id','product_id','quantity', 'datetime']
get_list = {c:eval('get_' + c) for c in columns}

trans_dict = {}

trans_cust = {}
product_info = {}
trans_dict = {}
trans_datetime = {}

for i in range(1,row_count + 1):   
    
    # Construct row
    
    row = {}
    for column in columns:
        row[column] = getter(column, row)
        
    # Add tp complete dictionary
    
    trans_dict[i] = row

 
trans_df = pd.DataFrame().from_dict(trans_dict, orient='index')
product_df = pd.DataFrame().from_dict(product_dict, orient='index')
product_df['product_id'] = product_df.index

flat = pd.merge(trans_df, product_df, on='product_id')