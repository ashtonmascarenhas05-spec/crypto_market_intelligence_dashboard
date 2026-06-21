import numpy as np
import pandas as pd 

class DataProcessor:
    def __init__(self,raw_data):
        self.raw_data = raw_data  # class receives a list of dictionaries from the scraper
        self.df = None   # we will store our clean dataframe here
        