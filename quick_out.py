#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  9 08:37:44 2017

@author: daniel
"""
import sys
import sqlite3

sys.path.append("../")
import datafairy as df

dtf = df.DataFairy()

flat = dtf.flat_file()

db = sqlite3.connect('datafairy.db')
flat.to_sql(name='flat_file', con=db, if_exists = 'replace')

