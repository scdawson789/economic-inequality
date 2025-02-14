import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import math

sns.set()

def calculate_cost_living(start, multiple, length):
    values = [start]
    for i in range(1, length):
        values.append(values[-1] * multiple)
    return values

pd.set_option('display.max_rows', None)
pd.set_option('display.expand_frame_repr', False)


# Median family income
median_family = pd.read_csv("data\\median_family_income_fred.csv", index_col=[0], header=0)
median_family.index = pd.to_datetime(median_family.index)
median_family = median_family.rename(columns={'MEFAINUSA646N': "median_family_income"})
median_family.index = median_family.index.year


start = 4242
cost_living = 1.0403
median_family['cost_of_living'] = calculate_cost_living(start, cost_living, len(median_family))

print(median_family)