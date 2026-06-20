import pandas as pd 

class DataProcessor:
    def __init__(self,raw_data):
        df = pd.DataFrame(raw_data)       ## Converting the raw data into panda dataframe
        print(df.isnull().sum()) ## checking null values in the raw_data
