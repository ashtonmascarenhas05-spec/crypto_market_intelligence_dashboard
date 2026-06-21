import numpy as np
import pandas as pd 

class DataProcessor:
    def __init__(self,raw_data):
        self.raw_data = raw_data  # class receives a list of dictionaries from the scraper
        self.df = None   # we will store our clean dataframe here
    def clean_data(self):
        df = pd.DataFrame(self.raw_data)     #It shall read the raw_data into a Pandas DataFrame
        df.fillna(0)          ## It fill the missing values with value 0
        df['TimeStamp'] = pd.Timestamp.now()    # Adding a TimeStamp
        self.df = df