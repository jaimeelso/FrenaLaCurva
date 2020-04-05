import numpy as np
import os
import pandas as pd
from datetime import datetime

DATA_FOLDER = os.path.dirname(os.getcwd()) + '/data/'

def split_data(values, test_size = 0.3, training_window = 1):
    longitud = len(values)
    test_size = int(test_size * longitud)
    train_size = longitud - test_size

    values = np.array(values)
    values_copy = values

    values, values_copy = create_window(X=values, y=values_copy, window=training_window)

    if test_size == 0:
        X_train = values
        X_test = []

        y_train = values_copy
        y_test = []

        X_train = np.reshape(X_train,(X_train.shape[0], training_window, 1))
    else:
        X_train = values[:train_size]
        X_test = values[train_size:]

        y_train = values_copy[:train_size]
        y_test = values_copy[train_size:]
    
        X_train = np.reshape(X_train,(X_train.shape[0], training_window, 1))
        X_test = np.reshape(X_test, (X_test.shape[0], training_window, 1))
    
    return X_train, X_test, y_train, y_test

def read_infected_csv(name,  poblation = 1, country = True):
    df = pd.read_csv(filepath_or_buffer = DATA_FOLDER + 'infected.csv')

    if country == True:
        selected_row = df.loc[df['Country/Region'] == name]
    else:
        selected_row = df.loc[df['Province/State'] == name]

    dates = list(df)[4:]

    if poblation == 1:
        simple_results = [float(selected_row[date].values[0]) for date in dates]
    else:
        simple_results = [round((float(selected_row[date].values[0])/poblation)*100,5) for date in dates]

    dates_formatted = [format_date(date = d) for d in dates]

    results = {}
    for i in range(len(dates)):
        results[dates_formatted[i]] = simple_results[i]

    return results, simple_results

def read_infected_spain_csv(ccaa):
    fname = DATA_FOLDER + '/infected_spain.csv'

    df = pd.read_csv(fname)

    ccaa = ccaa.upper()
    df['CCAA'] = [df['CCAA'][x].upper() for x in range(df.shape[0])]

    selected_row = df.loc[df['CCAA'] == ccaa]
    dates = list(df)[2:]

    simple_results = [float(selected_row[date].values[0]) for date in dates]

    results = {}
    for i in range(len(dates)):
        results[dates[i]] = simple_results[i]

    return results, simple_results

def format_date(date):
    datetime_object = datetime.strptime(date, '%m/%d/%y')
    string_object = datetime_object.strftime('%Y-%m-%d')
    return string_object

def balance_data(v1, v2):

    v1_balanced, v2_balanced = {}, {}

    for key in v1:
        try:
            if v2.get(key) != None:
                v2_balanced[key] = v2.get(key)
                v1_balanced[key] = v1.get(key)
        except KeyError:
            pass
    
    v1_simple = np.array([v1_balanced[key] for key in v1_balanced.keys()])
    v2_simple = np.array([v2_balanced[key] for key in v2_balanced.keys()])

    return v1_balanced, v2_balanced, v1_simple, v2_simple

def create_window(X, y, window = 1):

    new_X, new_y = [],[]
    period = []
    i = 0
    for inicio in range(len(X[:-window])):
        for i in range(window):
            period.append(X[inicio+i])

        
        new_X.append(period)
        i = 0
        period = []

    new_y = y[window:]

    return np.array(new_X), np.array(new_y)


    
