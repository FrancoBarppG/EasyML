
def least_squares (list_x, list_y):

    x = [int(n) for n in list_x]
    y = [int(n) for n in list_y]

    mean_x = sum(x)/len(x)
    mean_y = sum(y)/len(y)

    print('Mean X: ',mean_x)
    print('Mean Y: ',mean_y)

    if len(x)!=len(y):
        raise ValueError('Length of X and Y coordinates are different')
        return None

    #a = media y - b*media x
    #b = soma i pra n (xi - media x)*(yi - media y)/ soma 1 pra n(xi - media x)**2


    func_b = sum([x[i]*(y[i]-mean_y) for i in range(len(x))])/sum([x[i]*(x[i]-mean_x) for i in range(len(x))])
    func_a = mean_y - func_b*mean_x

    #TODO: ver pq tava trocado o a e o b no output quando colocquei a,b no app6

    return func_a, func_b
