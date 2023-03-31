import polars as pl
import os 

from time import time
from functools import wraps
from subgrounds.subgraph import SyntheticField
from subgrounds.subgraph.fieldpath import FieldPath



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

def synthetic_endpoint(endpoint) -> SyntheticField:
    return SyntheticField.constant(endpoint_name(endpoint))

def endpoint_name(endpoint):
    return endpoint.split('/')[-1]

def synthetic_convert(type, deps) -> SyntheticField:
    """
    Creates a new synthetic field path with a different type
    """
    match type:
        case SyntheticField.STRING:
            return SyntheticField(lambda value: str(value), SyntheticField.STRING, deps)
        case SyntheticField.INT:
            return SyntheticField(lambda value: int(value), SyntheticField.INT, deps)
        case SyntheticField.FLOAT:
            return SyntheticField(lambda value: float(value), SyntheticField.FLOAT, deps)
        case SyntheticField.BOOL:
            return SyntheticField(lambda value: bool(value), SyntheticField.BOOL, deps)

def save_file(df: pl.DataFrame, endpoint: str, saved_file_name: str = None):
    # check if data folder exists. If it doesn't, create it
    if not os.path.exists('../data'):
        os.makedirs('../data')

    if saved_file_name == None:
        df.write_parquet(f'data/{endpoint_name(endpoint)}.parquet')
    else:
        df.write_parquet(f'data/{saved_file_name}.parquet')   




