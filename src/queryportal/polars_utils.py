import pandas as pd
import polars as pl
import pyarrow as pa

from time import time
from functools import wraps

from typing import TYPE_CHECKING, Any


################################
# Python Decorators
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
            print(f'Schema: {output.schema}')
            return output
        except:
            print(f'TypeError: {output} is type {type(output)}. Must be polars DataFrame')
    return wrapper

############################
# Polars Support Functions
############################
def to_polars(df: pd.DataFrame):
    """
    NOTE - Currently not being used!

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


def fmt_dict_cols(df: pl.DataFrame) -> pl.DataFrame:
    """
    formats dictionary cols, which are 'structs' in a polars df, into separate columns and renames accordingly.
    """
    for column in df.columns:
        if isinstance(df[column][0], dict):  
            col_names = df[column][0].keys()
            # rename struct columns
            struct_df = df.select(
                pl.col(column).struct.rename_fields([f'{column}_{c}' for c in col_names])
            )
            struct_df = struct_df.unnest(column)
            # add struct_df columns to df and
            df = df.with_columns(struct_df)
            # drop the df column
            df = df.drop(column)
    
    return df

def fmt_arr_cols(df: pl.DataFrame) -> pl.DataFrame:
    """
    formats lists, which are arrays in a polars df, into separate columns and renames accordingly.
    Since there isn't a direct way to convert array -> new columns, we convert the array to a struct and then
    unnest the struct into new columns.
    """
    # use this logic if column is a list (rows show up as pl.Series)
    for column in df.columns:
        if isinstance(df[column][0], pl.Series):
            # convert struct to array
            struct_df = df.select([pl.col(column).arr.to_struct()])
            # rename struct fields
            struct_df = struct_df.select(
                pl.col(column).struct.rename_fields([f"{column}_{i}" for i in range(len(struct_df.shape))])
            )
            # unnest struct fields into their own columns
            struct_df = struct_df.unnest(column)
            # add struct_df columns to df and
            df = df.with_columns(struct_df)
            # drop the df column
            df = df.drop(column)

    return df






