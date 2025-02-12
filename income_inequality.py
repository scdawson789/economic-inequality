import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import math

#sns.set()

pd.set_option('display.max_rows', None)
pd.set_option('display.expand_frame_repr', False)


# Median family income
median_family = pd.read_csv("data\\median_family_income_fred.csv", index_col=[0], header=0)
median_family.index = pd.to_datetime(median_family.index)
median_family = median_family.rename(columns={'MEFAINUSA646N': "median_family_income"})
median_family.index = median_family.index.year

