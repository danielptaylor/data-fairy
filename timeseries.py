"""
@author: Daniel Taylor

TODO: Add exponential growth option
TODO: Make variance a function of growth, as it looks flat wth high growth, and a mess with low. or is this more realistic?

"""

import numpy as np
import pandas as pd
from datetime import timedelta, datetime
import json
import calendar as cal

class TimeSeries:
    
    def __init__(self, start_value=100000, annual_trend=0, 
                 variability=0.001, start_date="2014-01-01", days=900):     
        
        for a in ['start_value', 'variability', 'days']:            
            setattr(self, a, eval(a))        
        self.start_date = datetime.strptime(start_date,"%Y-%m-%d")
        self.annual_trend = np.random.normal(annual_trend, 0.07)
        
        self.time_series_dict = {}
        self.generate_time_series()
        self.weekday_adjust()
        self.checker = {}
        self.month_adjust()
        
        self.time_series_df = pd.DataFrame().from_dict(self.time_series_dict, orient='index')
        self.time_series_df.columns = ['value']        
    
    
    def generate_time_series(self):
        
        for i, datev in enumerate(self.get_date_range()):
            self.time_series_dict[datev] = self.get_date_value(i, datev)
            
        return None
        
        
    def get_date_range(self):
        
        return [self.start_date  + timedelta(days=i) for i in range(self.days)]
    
    
    def get_date_value(self, place, dateval):        
        
        growth_this = np.random.normal(0, self.variability)
    
        try:
            prev_value = self.time_series_dict[dateval - timedelta(days=1)]
            prev_prev_value = self.time_series_dict[dateval - timedelta(days=2)]
            prev_growth = (prev_value - prev_prev_value) / prev_prev_value
        except KeyError:
            prev_value = self.start_value
            prev_growth = growth_this
        
        multiplier = 1 + (self.annual_trend / 365) + (prev_growth / prev_value) + growth_this        
        
        return prev_value * multiplier
    
    
    def weekday_adjust(self):
        
        for i in self.time_series_dict.keys():
            rand_element = np.random.normal(1, 0.0001)
            weekday_element = self.get_weekday_adjust(i)
            
            self.time_series_dict[i] = self.time_series_dict[i] * rand_element * weekday_element
    
    
    def get_weekday_adjust(self, date_i):
        
        week_adjust = json.loads(open('defaults/time_1.json').read())['weekday']
        weekday_no = date_i.weekday()
        weekday_name = cal.day_name[weekday_no]
        this_adjust = week_adjust[weekday_name]
        
        dif = this_adjust - 1
        this_dif = np.random.normal(dif, 0.01) * 0.05
        
        return 1 + this_dif
    
    
    def month_adjust(self):
        
        for i in self.time_series_dict.keys():
            rand_element = np.random.normal(1, 0.0001)
            month_element = self.get_month_adjust(i)
            
            self.time_series_dict[i] = self.time_series_dict[i] * rand_element * month_element
    
    
    def get_month_adjust(self, date_i):      
        
        this_adjust = self.get_month_weighted_adjust(date_i)
                
        dif = this_adjust - 1
        this_dif = np.random.normal(dif, 0.01) * 0.05
                 
        return 1 + this_dif
        
    
    def get_month_weighted_adjust(self, day_i):
        
        if day_i.month == 12:
            prev_month = 'Nov'
            this_month = 'Dec'
            next_month = 'Jan'
        elif day_i.month == 1:            
            prev_month = 'Dec'
            this_month = 'Jan'
            next_month = 'Feb'
        else:
            prev_month = cal.month_abbr[day_i.month - 1]
            this_month = cal.month_abbr[day_i.month]
            next_month = cal.month_abbr[day_i.month + 1]
            
        month_len = cal.monthrange(day_i.year, day_i.month)[1]
        
        weights = {}
        
        weights[this_month] = 1 / abs(day_i.day - 15.01) 
        weights[prev_month] = 1 / (weights[this_month] + 15)
        weights[next_month] = 1 / (abs(day_i.day - month_len) + 15)
        
        sum_from = sum(weights.values())
        
        month_adjust = json.loads(open('defaults/time_1.json').read())['month']
        weight_list = [i / (sum_from) * month_adjust[k] for k, i in weights.items() if k != '']
        weight_adj = sum(weight_list)
        self.checker[day_i] = weight_list
                    
        return weight_adj
                
        
    def plot(self):
        self.time_series_df.plot()