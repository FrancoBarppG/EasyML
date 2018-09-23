import numpy as np
from sklearn import datasets, linear_model
import pandas as pd


def choose_reg_2d(dropdown, x, y):
    #########################################adicionar verificacao das lengths do x e y
    default = [0 for i in range(len(x))]
    if dropdown == 'lsm':
        x_2, y_2  = least_squares(x, y)
        return x_2, y_2
    elif dropdown == 'linear':
        x_2, y_2 =  linear_regression(x, y)
        return x_2, y_2
    elif dropdown == 'logi':
        x_2, y_2 = logistic_regression(x, y)
        return x_2, y_2
    elif dropdown == 'log':
        x_2, y_2 = logarithmic_regression(x, y)
        return x_2, y_2
    elif dropdown == 'exp':
        x_2, y_2 = exponential_regression(x, y)
        return x_2, y_2
    else:
        return default, default

def choose_reg_3d(dropdown, x, y, z):
    #########################################adicionar verificacao das lengths do x e y
    default = [0 for i in range(len(x))]
    if dropdown == 'linear3d':
        x_2, y_2, z_2 =  linear_regression_3d(x, y, z)
        return x_2, y_2, z_2
    elif dropdown == 'logi3d':
        x_2, y_2, z_2 =  logistic_regression_3d(x, y, z)
        return x_2, y_2, z_2
    else:
        return default, default, default


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

    # FIXME
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

def logarithmic_regression(x, y):

    print('\n-------Logarithmic Regression--------')

    #n = len(x)
    
    #func_b = (n*sum([y[i]*log(x[i]) for i in range(n)]) - sum(y)*sum([ log(x[i]) for i in range(n)]))/(sum([ log(x[i])**2 for i in range(n)]) - sum([ log(x[i]) for i in range(n)])**2)
    #func_a = (sum(y) - func_b*sum([ log(x[i]) for i in range(n)]))/n

    ################## TODO: ver se vou colocar opcao de weight no polyfit

    func_a, func_b = np.polyfit( np.log(np.array(x)), np.array(y), 1)
    x_2 = [i for i in range(int(max(x)))]
    y_2 = [(func_b + func_a*np.log(i)) if i>=1 else None for i in x_2]
    

    print('X: {}'.format(x_2))
    print('Y: {}'.format(y_2))

    return x_2, y_2

def exponential_regression(x, y):

    print('\n-------Exponential Regression--------')

    func_a, func_b = np.polyfit( np.array(x), np.log(np.array(y)), 1, w = 2*np.sqrt(y))
    x_2 = [i for i in range(int(max(x)))]
    y_2 = [(np.exp(func_b) * np.exp(func_a*i)) for i in x_2]

    print('X: {}'.format(x_2))
    print('Y: {}'.format(y_2))

    return x_2, y_2

def linear_regression_3d(df_x, df_y, df_z):

    print('\n-------Linar Regression 3d--------')
    
    #o z eh vertical inicialmente

    if len(df_x)>500:
        factor = 2 + 1*(len(df_x)/500 -1)
    else:
        factor = 1
        
    length_x = int(len(df_x)/factor)

    x_train = [[df_x[i], df_y[i]] for i in range(length_x)]
    z_train = df_z[:length_x]

    print(x_train)
    
    linreg = linear_model.LinearRegression()
    linreg.fit(x_train, z_train)


    data = [{'X': df_x[i], 'Y': df_y[i], 'Z': linreg.predict(x_train)[i]} for i in range(len(df_x))]
    df = pd.DataFrame(data)

    return df['X'], df['Y'], df['Z']


def logistic_regression_3d(df_x, df_y, df_z):

    print('\n-------Logistic Regression--------')

    if len(df_x)>500:
        factor = 2 + 1*(len(df_x)/500 -1)
    else:
        factor = 1

    length_x = int(len(df_x)/factor)

    x_train = [[df_x[i], df_y[i]] for i in range(length_x)]
    z_train = df_z[:length_x]
      
    logreg = linear_model.LogisticRegression()
    logreg.fit(x_train, z_train)


    data = [{'X': df_x[i], 'Y': df_y[i], 'Z': logreg.predict(x_train)[i]} for i in range(len(df_x))]
    df = pd.DataFrame(data)

    return df['X'], df['Y'], df['Z']



    
    



