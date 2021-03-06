"""
@author: Daniel Taylor

TODO: Add exponential growth option
TODO: Make variance a function of growth, as it looks flat wth high growth, and a mess with low. or is this actually more realistic?

"""

import numpy as np
import pandas as pd
from datetime import timedelta, datetime
import json
import calendar as cal
import os

class TimeSeries:
    
    def __init__(self, start_value=100000, annual_trend=0, 
                 variability=0.005, start_date="2014-01-01", days=900):     
        
        self.base_dir = os.path.dirname(__file__)
                                        
        for a in ['start_value', 'variability', 'start_date', 'days']:            
            setattr(self, a, eval(a))   
        
        if type(start_date) == str:
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
        
        random_element = np.random.normal(0, self.variability)
    
        try:
            prev_value = self.time_series_dict[dateval - timedelta(days=1)]
            prev_prev_value = self.time_series_dict[dateval - timedelta(days=2)]
            prev_growth = (prev_value - prev_prev_value) / prev_prev_value
        except KeyError:
            prev_value = self.start_value
            prev_growth = random_element
        
        multiplier = 1 + (self.annual_trend / 365) + (prev_growth / prev_value) + random_element        
        
        return prev_value * multiplier
    
    
    def weekday_adjust(self):
        
        for i in self.time_series_dict.keys():
            rand_element = np.random.normal(1, 0.0001)
            weekday_element = self.get_weekday_adjust(i)
            
            self.time_series_dict[i] = self.time_series_dict[i] * rand_element * weekday_element
    
    
    def get_weekday_adjust(self, date_i):
        
        week_adjust = json.loads(open(self.base_dir + '/defaults/time_1.json').read())['weekday']        
        weekday_name = cal.day_name[date_i.weekday()]
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
        
        month_i = day_i.month
        prev_month = cal.month_abbr[12 if month_i == 1 else month_i - 1]
        this_month = cal.month_abbr[month_i]
        next_month = cal.month_abbr[1 if month_i == 12 else month_i + 1]
            
        month_len = cal.monthrange(day_i.year, month_i)[1]
        
        weights = {}
        
        weights[this_month] = 1 / abs(day_i.day - 15.01) 
        weights[prev_month] = 1 / (weights[this_month] + 15)
        weights[next_month] = 1 / (abs(day_i.day - month_len) + 15)
        
        sum_from = sum(weights.values())
        
        month_adjust = json.loads(open(self.base_dir + '/defaults/time_1.json').read())['month']
        weight_list = [i / (sum_from) * month_adjust[k] for k, i in weights.items() if k != '']
        weight_adj = sum(weight_list)
        self.checker[day_i] = {'list':weight_list, 'actual': sum(weight_list)}
                    
        return weight_adj
    
    
    def get_daily_proportion(self):
        df = self.get_df()
        daily_proportion = df['value'].apply(lambda x: (x / sum(df['value'])))
        
        return daily_proportion
    
    
    """
    Bit of convenience
    """
                
        
    def plot(self):
        self.time_series_df.plot()
        
        
    def get_df(self):
        return self.time_series_df
    