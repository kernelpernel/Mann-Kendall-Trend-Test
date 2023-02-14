"""
Script to conduct Mann-Kendall trend test on a timeseries data set.

Author: Ethan Purnell
Date: 1/23/23
"""

import pandas as pd
import math
import scipy
import statistics


def read_data(filename, sheet=0):
    # Could probably change this to read through all files in a folder
    if '.csv' in filename:
        data = pd.DataFrame(pd.read_csv(filename))

    elif '.xlsx' in filename:
        data = pd.DataFrame(pd.read_excel(filename, sheet_name=sheet, index_col=0, header=0))

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
    n = len(timeseries_list)
    results = []
    i = 0

    for item in timeseries_list:
        j = i + 1

        while j < n:
            entry = sign(timeseries_list[j] - item)
            results.append(entry)
            j += 1

        i += 1

    S = sum(results)
    tau_denom = (n * (n - 1)) / 2
    tau = S / tau_denom

    return S, tau


def calculate_sigma_s(timeseries_list):
    # Currently assumes no ties, will build functionality in later if needed
    n = len(timeseries_list)
    radicand = (n/18)*(n-1)*(2*n + 5)

    return math.sqrt(radicand)


def calculate_Z_statistic(S, sigma_s):
    if S > 0:
        return (S - 1) / sigma_s

    elif S < 0:
        return (S + 1) / sigma_s

    else:
        return 0


def calculate_p_value(z, one_tailed=True):
    if one_tailed:
        return scipy.stats.norm.sf(abs(z))

    else:
        return scipy.stats.norm.sf(abs(z)) * 2


def analyze_trend(stats_dict):
    for key, value in stats_dict.items():
        S = value[0]
        tau = round(value[1], 3)
        CF = round(value[4], 5)
        CoV = value[6]
        if S > 0:
            if CF > 0.95:
                print(key)
                print('Trend Result: Increasing')
                print('Test Statistics: S = ' + str(S) + ', Tau = ' + str(tau) + ', CF = ' + str(CF*100) + '%')
                print('\n')

            if 0.95 >= CF >= 0.9:
                print(key)
                print('Trend Result: Probably Increasing')
                print('Test Statistics: S = ' + str(S) + ', Tau = ' + str(tau) + ', CF = ' + str(CF*100) + '%')
                print('\n')

            if CF < 0.9:
                print(key)
                print('Trend Result: No Trend')
                print('Test Statistics: S = ' + str(S) + ', Tau = ' + str(tau) + ', CF = ' + str(CF*100) + '%')
                print('\n')

        if S <= 0:
            if CF < 0.9 and CoV >= 1:
                print(key)
                print('Trend Result: No Trend')
                print('Test Statistics: S = ' + str(S) + ', Tau = ' + str(tau) + ', CF = ' + str(CF*100) + '%')
                print('\n')

            if CF < 0.9 and CoV < 1:
                print(key)
                print('Trend Result: Stable')
                print('Test Statistics: S = ' + str(S) + ', Tau = ' + str(tau) + ', CF = ' + str(CF*100) + '%')
                print('\n')

        if S < 0:
            if CF > 0.95:
                print(key)
                print('Trend Result: Decreasing')
                print('Test Statistics: S = ' + str(S) + ', Tau = ' + str(tau) + ', CF = ' + str(CF*100) + '%')
                print('\n')

            if 0.95 >= CF >= 0.9:
                print(key)
                print('Trend Result: Probably Decreasing')
                print('Test Statistics: S = ' + str(S) + ', Tau = ' + str(tau) + ', CF = ' + str(CF*100) + '%')
                print('\n')


def MKtest(data):

    column_stats = {}

    for column, values in data.items():
        if column == 'Year':
            X = list(values.values)
            continue
        else:
            values.dropna(inplace=True)
            items = list(values.values)
            S, tau = calculate_test_statistics(items)
            # The z-stat only valid if n > 10. Will build in later if needed. Some data sets have n = 10... will just
            # assume for now that they meet the requirements for this
            sigma_s = calculate_sigma_s(items)
            z = calculate_Z_statistic(S, sigma_s)
            p = calculate_p_value(z)
            CF = 1-p
            mean = sum(items) / len(items)
            CoV = statistics.stdev(items) / mean
            entry = {column: [S, tau, sigma_s, z, CF, p, CoV]}
            column_stats.update(entry)

    return column_stats


data = read_data('$FILENAME$')
data = data.iloc[5:, :]
column_stats = MKtest(data)
analyze_trend(column_stats)