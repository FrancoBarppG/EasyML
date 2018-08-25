import numpy as np
from sklearn import datasets, linear_model
import pandas as pd


def choose_reg(dropdown, x, y):
    default = [0 for i in range(len(x))]
    if dropdown == 'lsm':
        x_2, y_2  = least_squares(x, y)
        return x_2, y_2
    elif dropdown == 'linear':
        x_2, y_2 =  linear_regression(x, y)
        return x_2, y_2
    elif dropdown == 'log':
        x_2, y_2 = logistic_regression(x, y)
        return x_2, y_2
    else:
        return default, default


def least_squares (list_x, list_y):

    print('\n-------Least Squares--------')

    x = [int(n) for n in list_x]
    y = [int(n) for n in list_y]

    mean_x = sum(x)/len(x)
    mean_y = sum(y)/len(y)

    print('Mean X: ',mean_x)
    print('Mean Y: ',mean_y)

    if len(x)!=len(y):
        raise ValueError('Length of X and Y coordinates are different')
        return None


    func_b = sum([x[i]*(y[i]-mean_y) for i in range(len(x))])/sum([x[i]*(x[i]-mean_x) for i in range(len(x))])
    func_a = mean_y - func_b*mean_x

    x_2 = [i for i in range(int(max(x)))]
    y_2 = [(func_b*x_2[i] + func_a) for i in range(max(x))] ############# o a e b tao trocado de proposito
    

    return x_2, y_2




def linear_regression(df_x, df_y):

    print('\n-------Linar Regression--------')
    print(df_x)
    print(df_y)

    df_x = df_x.values.reshape(len(df_x),1)
    df_y = df_y.values.reshape(len(df_y),1)

    if len(df_x)>500:
        factor = 2 + 1*(len(df_x)/500 -1)
    else:
        factor = 1

        
    length_x = int(len(df_x)/factor)
    length_y = int(len(df_y)/factor)

    x_train = df_x[:length_x]
    x_test = df_x[length_x:]

    y_train = df_y[:length_y]
    y_test = df_y[length_y:]
    
    
    linreg = linear_model.LinearRegression()
    linreg.fit(x_train, y_train)


    data = [{'X': df_x[i][0], 'Y': linreg.predict(df_x)[i][0], 'Z': None} for i in range(len(df_x))]
    df = pd.DataFrame(data)

    return df['X'], df['Y']

def logistic_regression(df_x, df_y):

    print('\n-------Logistic Regression--------')
    print(df_x)
    print(df_y)

    df_x = df_x.values.reshape(len(df_x),1)
    df_y = df_y.values.reshape(len(df_y),1)

    if len(df_x)>500:
        factor = 2 + 1*(len(df_x)/500 -1)
    else:
        factor = 1


    length_x = int(len(df_x)/factor)
    length_y = int(len(df_y)/factor)

    x_train = df_x[:length_x]
    x_test = df_x[length_x:]

    y_train = df_y[:length_y]
    y_test = df_y[length_y:]
    
    
    logreg = linear_model.LogisticRegression()
    logreg.fit(x_train, y_train)


    data = [{'X': df_x[i][0], 'Y': logreg.predict(df_x)[i], 'Z': None} for i in range(len(df_x))]
    df = pd.DataFrame(data)

    return df['X'], df['Y']




