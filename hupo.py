from multiprocessing import Pool

def f(x,y):
    return x*y, 2

a, = f(2,2)
print(a)