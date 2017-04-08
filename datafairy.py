"""
@author: Daniel Taylor

Generate 'random' data with underlying correlations and other non random features

TODO: Add capability to radar to specify time of day and week weightings
TODO: Create customer dict before trans - probs easier to create correlations this way
TODO: Add non-randomness
TODO: Add region information
TODO: Add market information, i.e. for region / demographics
TODO: parameterize dates
"""

import numpy as np
import pandas as pd
import random
import json
from datetime import datetime, timedelta
import datetime as dt
import timeseries as ts
import calendar as cal
import os


class DataFairy:
    
    def __init__(self, nrows = 1000000, trans_per_customer = 5, products_per_transaction = 3, 
                 product_count = 1000, start_date = "2014-01-01", days = 730, annual_trend = 0.1):        
        
        args = ['nrows','trans_per_customer','products_per_transaction','product_count','days', 'annual_trend']
        
        for a in args:            
            setattr(self, a, eval(a))        
        
        self.customer_count = self.nrows / self.trans_per_customer
        self.start_date = datetime.strptime(start_date,"%Y-%m-%d")        
        self.end_date = self.start_date + timedelta(days=days)
        
        self.daily_allocation = None
        self.daily_proportion = None
        self.month_day_selection = {}
        self.base_dir = os.path.dirname(__file__)
        
        unique_days = [self.start_date + timedelta(days=x) for x in range(0, days)]
        unique_months = list(set([i.replace(day=1) for i in unique_days]))
        
        for i in unique_months:
            self.month_day_selection[i] = None
        
        self.demographics = json.loads(open(self.base_dir + '/defaults/customer_1.json').read())
        
        self.product_dict = self.build_product_table()
        self.transaction_dict = self.build_transaction_data()    
        
        print("Creating dataframes ...")
        self.product_df = pd.DataFrame().from_dict(self.product_dict, orient='index')
        self.product_df['product_id'] = self.product_df.index
        self.transaction_df = pd.DataFrame().from_dict(self.transaction_dict, orient='index')        
        
        print("WARNING: Data currently won't have all non-random features. Work in progress")
    
    
    def build_product_table(self):
       
        self.category_tree = json.loads(open(self.base_dir + '/defaults/product_1.json').read())
        ct = self.category_tree
        total_prop = sum([ct[c]['prop_size'] for c in ct.keys()])
        
        product_id = 0
        product_dict = {}
        
        for c, values in ct.items():
            category_size = round(values['prop_size'] / total_prop * self.nrows)
            
            for i in range(0,category_size):
                
                subs = ct[c]['sub']
                count = len(subs)-1
                sub = subs[random.randint(0, count)]
                price = max(np.random.normal(ct[c]['average_price'], 10), 5)
                
                product_dict[product_id] = {'category': c, 'sub_category': sub, 'price': price}
                product_id += 1
                
        print("Product table built")
                
        return product_dict
    
    
    def build_transaction_data(self):
        
        columns = ['transaction_id','customer_id','product_id','quantity', 'datetime']
        self.get_list = {c:getattr(self,'get_' + c) for c in columns}
        
        trans_dict = {}
        self.trans_cust = {}
        self.trans_datetime = {}
        
        for i in range(1,self.nrows + 1):
            
            row = {}
            for column in columns:
                row[column] = self.getter(column, row)
            
            trans_dict[i] = row        
                      
            if self.nrows >= 100000 and i % 100000 == 0:
                print(str(i) + " rows generated | " + str(i / self.nrows * 100) + "%")
        
        return trans_dict
    
    
    def getter(self, column, args):
    
        return self.get_list[column](args)


    def get_product_id(self,args):
        
        return random.randint(0,len(self.product_dict.keys()) - 1)
    
    
    def get_transaction_id(self, args):
        trans_per_customer = self.trans_per_customer
        count = trans_per_customer * self.customer_count
        
        return random.randint(1,count)
    
    
    def get_customer_id(self, args):    
           
        try:        
            # Get existing customer_id for transaction if exists
            customer_id = self.trans_cust[args['transaction_id']]
            
        except KeyError:        
            customer_id = random.randint(1,self.customer_count)
            self.trans_cust[args['transaction_id']] = customer_id        
        
        return customer_id
    
    
    def get_datetime(self, args):
        
        try:
            # Get existing datetime for transaction if exists
            row_date = self.trans_datetime[args['transaction_id']]
            self.daily_allocation[row_date] -= 1
            return row_date
        
        except KeyError:
            # Generate pseudo random date it no date exists for transaction
            
            if self.daily_allocation == None:
                time_s = ts.TimeSeries(days=self.days, start_date = self.start_date, annual_trend = self.annual_trend)
                self.daily_proportion = time_s.get_daily_proportion()
                self.daily_allocation = self.daily_proportion * (self.nrows)
                self.daily_allocation = self.daily_allocation.to_dict()
                
            try:
                row_date = random.choice(list(self.daily_allocation.keys()))
                
                if self.daily_allocation[row_date] <= 0:
                    self.daily_allocation.pop(row_date,None)                
                self.daily_allocation[row_date] -= 1
                                     
            except KeyError:                
                row_date = random.choice(self.daily_proportion.index)
            
            self.trans_datetime[args['transaction_id']] = row_date
                                           
            return row_date
        
        
    def get_quantity(self, args):
        
        return max(round(np.random.normal(1.2,0.5)),1)
    
    

    """
    Convenience
    """
    
    def flat_file(self):
        return pd.merge(self.transaction_df, self.product_df, on='product_id')