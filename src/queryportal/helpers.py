import pandas as pd
import polars as pl
import pyarrow as pa

from time import time
from functools import wraps, cache
from subgrounds import Subgrounds
from subgrounds.subgraph import SyntheticField
from subgrounds.subgraph.fieldpath import FieldPath
from subgrounds.schema import TypeRef

from typing import TYPE_CHECKING, Any, Optional


################################
# Query Decorator Functions
################################
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

############################
# Polars Support Functions
############################
def to_polars(df: pd.DataFrame):
    """
    Use to convert a pandas dataframe to a polars dataframe. Iterates over every pandas column and checks for
    OverflowErrors. If an OverflowError is encountered, the column is converted to a float type.
    """
    for column in df.columns:
        try:
            pa.array(df[column])
        except OverflowError:
            print(f"OverflowError encountered in column {column}. Converting to float type...")
            df[column] = df[column].astype(float)
        except KeyError:
            print(f'KeyError encountered in column {column}, passing along...')
    return pl.from_pandas(df)

def save_file(df: pl.DataFrame, saved_file_name: str = None):
    """
    Saves a polars DataFrame to a parquet file. If no file name is specified, the file name will be the endpoint name.
    """
    if saved_file_name is not None:
        df.write_parquet(f'{saved_file_name}.parquet')


##############################################
# Synthetic Field Helper Creation Functions
##############################################
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
        

@cache
def get_subgrounds():
    """
    Returns a `Subgrounds` object representing a collection of subgrounds. The `@cache` decorator
    ensures that the `Subgrounds` object returned by this function is cached and returned on subsequent
    calls to this function, rather than being recomputed every time. 

    """
    return Subgrounds()

def match_query_paths(default_query_path: FieldPath, query_paths: list[str] = None) -> FieldPath | list[FieldPath]:
    """
    Matches query_paths to query_path_cols
    """
    match query_paths:
        case None:
            return default_query_path
        case _:
            return [
                default_query_path._select(field) for field in query_paths
            ]