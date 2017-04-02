"""
@author: Daniel Taylor

Generate 'random' data with underlying correlations and other non random features

TODO: parameterize dates and cutomer_count
TODO: Add capability to radar to specify time of day and week weightings
TODO: Tidy arg setters. Looks gross in init
TODO: Create customer dict before trans - probs easier to create correlations this way
TODO: Add non-randomness

"""

import numpy as np
import pandas as pd
import random
import json
from datetime import datetime
import radar

class DataFairy:
    
    def __init__(self, category_tree='Default', nrows = 10000, trans_per_customer = 5, products_per_transaction = 3, product_count = 100):
        
        args = ['category_tree','nrows','trans_per_customer','products_per_transaction','product_count']
        
        for a in args:            
            setattr(self, a, eval(a))
            
        self.customer_count = self.nrows / 5
        self.date_min = datetime(2007, 1, 1)
        self.date_max = datetime(2017, 4, 2)

        
        if self.category_tree == 'Default':
            self.category_tree = json.loads(open('product_tables/default.json').read())
        
        self.product_dict = self.build_product_table()
        self.transaction_dict = self.build_transaction_data()    
        
        print("Creating dataframes ...")
        self.product_df = pd.DataFrame().from_dict(self.product_dict, orient='index')
        self.product_df['product_id'] = self.product_df.index
        self.transaction_df = pd.DataFrame().from_dict(self.transaction_dict, orient='index')
        self.flat_file = pd.merge(self.transaction_df, self.product_df, on='product_id')
        
        print("WARNING: Data currently won't have non-random features. Work in progress")
    
    
    def build_product_table(self):
       
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
            return self.trans_datetime[args['transaction_id']]
        
        except KeyError:        
            row_datetime =  radar.random_datetime(self.date_min, self.date_max)        
            self.trans_datetime[args['transaction_id']] = row_datetime
            return row_datetime
        
        
    def get_quantity(self, args):
        
        return random.randint(1,3)