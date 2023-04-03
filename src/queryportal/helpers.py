import pandas as pd
import polars as pl
import pyarrow as pa

from time import time
from functools import wraps
from subgrounds.subgraph import SyntheticField
from subgrounds.subgraph.fieldpath import FieldPath



def timeit(func):
    """
    Decorator used to how long a query takes
    """
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
    Decorator that describes the basic properties of a polars DataFrame output - the shape, columns, datatypes, and header
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

def to_polars(df: pd.DataFrame):
    """
    Use to convert a pandas dataframe to a polars dataframe. Iterates over every pandas column and checks for
    OverflowErrors. If an OverflowError is encountered, the column is converted to a float type.
    """
    for column in df.columns:
        print(column)
        try:
            pa.array(df[column])
        except OverflowError:
            print(f"OverflowError encountered in column {column}. Converting to float type...")
            df[column] = df[column].astype(float)
    return pl.from_pandas(df)

def save_file(df: pl.DataFrame, saved_file_name: str = None):
    """
    Saves a polars DataFrame to a parquet file. If no file name is specified, the file name will be the endpoint name.
    """
    if saved_file_name is not None:
        df.write_parquet(f'{endpoint_name(saved_file_name)}.parquet')


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





