import numpy as np
import pandas as pd 

class DataProcessor:
    def __init__(self,raw_data):
        self.raw_data = raw_data  # class receives a list of dictionaries from the scraper
        self.df = None   # we will store our clean dataframe here
    def clean_data(self):
        # 1. Create an empty list to hold our flat, clean dictionaries
        flat_data = []
        
        # 2. Dig into the messy raw data and extract ONLY what we need
        for item in self.raw_data:
            try:
                flat_record = {
                    'coin': item.get('name', 'Unknown'),
                    'price': item['market_data']['current_price']['usd'] # Digging deep for the price!
                }
                flat_data.append(flat_record)
            except KeyError:
                # If a record failed or is missing this structure, skip it gracefully
                continue

        # 3. NOW we convert our perfectly flat list into a DataFrame
        df = pd.DataFrame(flat_data)     
        
        # 4. Standardize and Timestamp
        df = df.fillna(0)                     
        df['timestamp'] = pd.Timestamp.now()  
        
        self.df = df
    def add_features(self):
        df = self.df
        
        # Safe Logarithm, If price is greater than 0, calculate log. Otherwise, set to 0.
        df['log_price'] = np.where(df['price'] > 0, np.log(df['price']), 0)
        
        # Getting Minimum and Maximum values
        max_price = df['price'].max()
        min_price = df['price'].min()

        # Safe Normalization, Check for zero division before calculating
        if max_price == min_price:
            df['normalized_price'] = 0.5  # If all prices are the same, default to the middle
        else:
            df['normalized_price'] = (df['price'] - min_price) / (max_price - min_price)
            
        self.df = df
    
    # A generator that yields one row of the dataframe at a time
    def stream_rows(self):
        for row in self.df.itertuples(index=False):
            yield row