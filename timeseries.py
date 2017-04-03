"""
@author: Daniel Taylor

TODO: Add exponential growth option

"""

import numpy as np
import pandas as pd
from datetime import timedelta, datetime

class TimeSeries:
    
    def __init__(self, start_value=100000, annual_trend=0, 
                 variability=0.001, start_date="2014-01-01", days=900):     
        
        for a in ['start_value', 'variability', 'days']:            
            setattr(self, a, eval(a))
        
        self.start_date = datetime.strptime(start_date,"%Y-%m-%d")
        self.annual_trend = np.random.normal(annual_trend, 0.07)
        self.time_series_dict = {}
        self.generate_time_series()
        
        self.time_series_df = pd.DataFrame().from_dict(self.time_series_dict, orient='index')
        self.time_series_df.columns = ['value']
    
    
    def generate_time_series(self):
        
        for i, datev in enumerate(self.get_date_range()):
            self.time_series_dict[datev] = self.get_date_value(i, datev)
        
        
    def get_date_range(self):
        
        return [self.start_date  + timedelta(days=i) for i in range(self.days)]
    
    
    def get_date_value(self, place, dateval):
        
        growth_this = np.random.normal(0, self.variability)  
    
        try:
            prev_value = self.time_series_dict[dateval - timedelta(days=1)]
            prev_growth = self.time_series_dict[dateval - timedelta(days=2)] / prev_value
        except KeyError:
            prev_value = self.start_value
            prev_growth = 0
        
        multiplier = 1 + (self.annual_trend / 365) + (prev_growth / prev_value) + growth_this        
        
        return prev_value * multiplier