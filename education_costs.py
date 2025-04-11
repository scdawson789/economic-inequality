import pandas as pd
import numpy as np

skip_rows = list(range(0,1)) + list(range(48,51))
data = pd.read_csv("data/college_inflation.csv", skiprows=skip_rows, header=0 )
grouped = data.groupby('Year').agg()
#https://www.usinflationcalculator.com/inflation/college-tuition-inflation-in-the-united-states/