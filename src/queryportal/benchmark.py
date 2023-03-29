from time import time
from functools import wraps


def timeit(func):
    # This function shows the execution time of the function object passed.
    def wrap_func(*args, **kwargs):
        t1 = time()
        result = func(*args, **kwargs)
        t2 = time()
        print(f'Function {func.__name__!r} executed in {(t2-t1):.4f}s')
        return result
    return wrap_func


def df_describe(function):
    """
    Describes basic properties of a polars DataFrame output - the shape, columns, datatypes, and header
    """
    @wraps(function)
    def wrapper(*args, **kwargs):
        output = function(*args, **kwargs) # should be a pl.DataFrame
        # try except: if it's a dataframe, print the shape. If the function crashes, print the error message.
        try:
            print(f'Shape: {output.shape}')
            print(f'Column Names: {output.columns}')
            print(f'Data Types: {output.dtypes}')
            print(f'Data: \n{output.head(5)}')

            return output
        except:
            print(f'TypeError: {output} is type {type(output)} and not a polars DataFrame')
    return wrapper