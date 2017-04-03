#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 22:01:21 2017

@author: daniel
"""

from timeseries import TimeSeries
import json

class SalesBreakdown:
    
    def __init__(self):
        
        ts = TimeSeries(days=365)
        self.timeseries_df = ts.time_series_df
        
    
    def get_breakdowns(self):
        
        self.category_tree = json.loads(open('defaults/product_1.json').read())
        self.demographics = json.loads(open('defaults/customer_1.json').read())
        
        
