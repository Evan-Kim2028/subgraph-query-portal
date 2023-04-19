from abc import ABC, abstractmethod
from queryportal.helpers import *

class QueryInterface(ABC):
    """
    The QueryInterface abstract class provides a standard interface for querying data from a data source. 
    By defining the query method as abstract, it forces any class that inherits from QueryInterface to implement its own version of the query method, 
    which ensures that all implementing classes have a consistent API. 
    Additionally, the class includes decorators such as @timeit and @df_describe which add additional functionality to the query method.
    """

    @abstractmethod
    @timeit  # Decorator that times the execution of the query method
    @df_describe  # Decorator that adds a description of the returned dataframe to the console
    def query(
            self, 
            query_path: FieldPath | list[FieldPath],
            saved_file_name: str = None,
            add_endpoint_col: bool = True
            ) -> pl.DataFrame:
        """
        new query method that uses query_json() instead of query_df(). Placeholder comment.
        """
        # Obtain json dict
        df = self.sg.query_json(query_path)

        # get nested json key. Subgrounds creates a hash blob for internal purposes so we need the keys that come after the hash blob.
        first_key = next(iter(df[0].keys()))

        pl_df = pl.from_dicts(df[0][first_key])

        pl_df = fmt_dict_cols(pl_df)
        final_df = fmt_arr_cols(pl_df)

        # If a file name is provided, save the dataframe as a CSV file
        if saved_file_name is not None:
            save_file(final_df, saved_file_name)

        # Return the converted dataframe
        return final_df
    

# OLD query() method! Saving just incase...
    # @abstractmethod
    # @timeit  # Decorator that times the execution of the query method
    # @df_describe  # Decorator that adds a description of the returned dataframe to the console
    # def query(
    #         self, 
    #         query_path: FieldPath | list[FieldPath],
    #         saved_file_name: str = None,
    #         add_endpoint_col: bool = True
    #         ) -> pl.DataFrame:
    #     """
    #     Abstract query method. Requires the following:
    #     - query path: A string representing the query to be executed

    #     The query method is responsible for obtaining query results from a data source, converting the results to a pandas dataframe, and returning the dataframe.
    #     """

    #     # Obtain pandas dataframe of query results
    #     df = self.sg.query_df(query_path)

    #     # Convert dataframe to Polars dataframe
    #     converted_df = to_polars(df)

    #     # If a file name is provided, save the dataframe as a CSV file
    #     if saved_file_name is not None:
    #         save_file(converted_df, saved_file_name)

    #     # Return the converted dataframe
    #     return converted_df

    
    def add_synthetic_fields(self):
        """
        Add all synthetic fields for token entities here
        """
        pass
