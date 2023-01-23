"""
Script to conduct Mann-Kendall trend test on a timeseries data set.

Author: Ethan Purnell
Date: 1/23/23
"""

import pandas as pd


def read_data():
    # Could probably change this to read through all files in a folder
    data = pd.DataFrame(pd.read_csv('Excavation Damages.csv'))

    return data

# def build_selection_menu(): would like to use this to read the columns and allow the user to choose which one they
# get the test info for


def sign(x):
    if x > 0:
        return 1

    if x == 0:
        return 0

    if x < 0:
        return -1


def calculate_test_statistics(timeseries_list):
    n = len(items)
    results = []

    for item in items:
        i = items.index(item)
        j = i + 1

        while j < n:
            entry = sign(items[j] - item)
            results.append(entry)
            j += 1

    S = sum(results)
    tau_denom = (n * (n - 1)) / 2
    tau = S / tau_denom

    return S, tau


data = read_data()

column_S_values = {}

for column, values in data.items():
    if column == 'Year':
        X = list(values.values)
        continue
    else:
        values.dropna(inplace=True)
        items = list(values.values)
        S, tau = calculate_test_statistics(items)
        entry = {column: [S, tau]}
        column_S_values.update(entry)
# print(X)

print(column_S_values)

