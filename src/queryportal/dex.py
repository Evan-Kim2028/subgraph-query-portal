import polars as pl

from dataclasses import dataclass, field
from subgrounds import Subgrounds
from subgrounds.schema import TypeRef
from subgrounds.subgraph import Subgraph
from subgrounds.subgraph import SyntheticField
from queryportal.helpers import *
from queryportal.queryinterface import QueryInterface

@dataclass
class Dex(QueryInterface):
    """
    DEX class stores standardized Messari DEX query methods for easier access. 
    The queries assume that Messari schemas and may not function properly if used with non-Messari standardized Dex subgraphs.
    """
    endpoint: str
    subgraph: Subgraph = None
    sg: Subgrounds = field(default_factory=get_subgrounds) 
    # NOTE: By default, this function returns the `Subgrounds` object with default settings. If you want to 
    # customize the subgrounds collection, you can pass a `Subgrounds` object with your desired settings
    # to the function as the `default_fact` parameter. This allows you to use a header for the subgrounds
    # collection.


    def __post_init__(self):
        # load dex subgraph schema information from the the subgraph endpoint. This is represented as a Subgraph object.
        self.subgraph = self.sg.load(self.endpoint)

        # add synthetic fields to the subgraph schema at initialization
        self.add_synthetic_fields()

    def query(
            self, 
            query_path: FieldPath | list[FieldPath],
            saved_file_name: str = None,
            add_endpoint_col: bool = True
            ) -> pl.DataFrame:
        """
        Concrete implementation of the abstract query method. Requires query_path as an input.
        """

        # obtain pandas dataframe of query results
        df = self.sg.query_df(query_path)

        converted_df = to_polars(df)

        if saved_file_name is not None:
            save_file(converted_df, saved_file_name)

        return converted_df
    
    def add_synthetic_fields(self):
        """
        Add all synthetic fields for the subgraph endpoint here, to be instantiated at initialization.
        """
        # swaps entity has a timestamp integer column. We convert that to datetime format using a synthetic field.
        self.subgraph.Swap.datetime = SyntheticField.datetime_of_timestamp(self.subgraph.Swap.timestamp)

        # # add synthetic endpoints
        self.subgraph.Swap.endpoint = SyntheticField.constant(self.endpoint.split('/')[-1])
        self.subgraph.Token.endpoint = SyntheticField.constant(self.endpoint.split('/')[-1])
        self.subgraph.LiquidityPool.endpoint = SyntheticField.constant(self.endpoint.split('/')[-1])


    @timeit
    @df_describe
    def query_swaps(self, query_paths: list[str] = None, query_size=5, filter_dict={}, saved_file_name=None, add_endpoint_col=True) -> pl.DataFrame:
        """
        This method allows query construction from the Swap entity. It takes in query parameters as inputs and returns a 
        Polars DataFrame of the query results. The method also adds a datetime column to the swaps entity by converting the 
        timestamp column to datetime format using a synthetic field. The `add_endpoint_col` parameter is used to add the 
        endpoint column to the query results if set to True.
        """

        # define query search params based off of filter_dict
        swaps_qp = self.subgraph.Query.swaps(
            first=query_size,
            orderBy=self.subgraph.Query.swaps.timestamp,
            orderDirection='desc',
            where = filter_dict
        )

        matched_query_path = match_query_paths(query_paths=query_paths, default_query_path = swaps_qp)
        return self.query(
                    query_path=matched_query_path,
                    saved_file_name=saved_file_name,
                    add_endpoint_col=add_endpoint_col
                )
            

    @timeit
    @df_describe
    def query_tokens(self, query_size=5, query_paths: list[str] = None, filter_dict={}, saved_file_name=None, add_endpoint_col=True) -> pl.DataFrame:
        """
        Runs a query against the tokens schema
        """
        # define query search params based off of filter_dict
        tokens_qp = self.subgraph.Query.tokens(
            first=query_size,
            where = filter_dict
        )

        matched_query_path = match_query_paths(query_paths=query_paths, default_query_path = tokens_qp)
        return self.query(
                    query_path=matched_query_path,
                    saved_file_name=saved_file_name,
                    add_endpoint_col=add_endpoint_col
                )


    @timeit
    @df_describe
    def query_pools(self, query_size=5, query_paths: list[str] = None, filter_dict={}, saved_file_name=None, add_endpoint_col=True) -> pl.DataFrame:
        """
        Runs a query against the liquiditypools entity
        """
        
        # define query search params based off of filter_dict
        pools_qp = self.subgraph.Query.liquidityPools(
            first=query_size,
            where = filter_dict
        )

        matched_query_path = match_query_paths(query_paths=query_paths, default_query_path = pools_qp)
        return self.query(
                    query_path=matched_query_path,
                    saved_file_name=saved_file_name,
                    add_endpoint_col=add_endpoint_col
                )
    
    @timeit
    @df_describe
    def query_firehose(self, query_size=5, query_paths: list[str] = None, filter_dict={}, saved_file_name=None, add_endpoint_col=True) -> pl.DataFrame:
        """
        Runs a query against the firehose entity
        """

        #################################################################################################################
        # PUT ALL THIS SHIT INTO ANOTHER FUNCTION? Like a pre-compute merge
        # 1. run token and pools query to get id info for joining
        token_query_cols = ['id', 'name', 'symbol', 'decimals']
        pool_query_cols = ['id', 'name', 'symbol']

        token_df = self.query_tokens(query_size=10000, query_paths=token_query_cols)
        pool_df = self.query_pools(query_size=10000, query_paths=pool_query_cols)

        # create a dictionary of token ids and their symbols
        token_symbol_dict = dict(zip(token_df['tokens_id'], token_df['tokens_symbol']))
        token_decimal_dict = dict(zip(token_df['tokens_id'], token_df['tokens_decimals']))
        token_name_dict = dict(zip(token_df['tokens_id'], token_df['tokens_name']))

        # create a dictionary of pool ids and their tokens
        pool_name_dict = dict(zip(pool_df['liquidityPools_id'], pool_df['liquidityPools_name']))
        pool_symbol_dict = dict(zip(pool_df['liquidityPools_id'], pool_df['liquidityPools_symbol']))

        # left inner joins between swaps and tokens
        self.subgraph.Swap.tokenIn_symbol = SyntheticField.map(token_symbol_dict, SyntheticField.STRING, self.subgraph.Swap.tokenIn.id, "uknown")
        self.subgraph.Swap.tokenOut_symbol = SyntheticField.map(token_symbol_dict, SyntheticField.STRING, self.subgraph.Swap.tokenOut.id, "uknown")
        self.subgraph.Swap.tokenIn_decimals = SyntheticField.map(token_decimal_dict, SyntheticField.INT, self.subgraph.Swap.tokenIn.id, 0)
        self.subgraph.Swap.tokenOut_decimals = SyntheticField.map(token_decimal_dict, SyntheticField.INT, self.subgraph.Swap.tokenOut.id, 0)
        self.subgraph.Swap.tokenIn_name = SyntheticField.map(token_name_dict, SyntheticField.STRING, self.subgraph.Swap.tokenIn.id, "uknown")
        self.subgraph.Swap.tokenOut_name = SyntheticField.map(token_name_dict, SyntheticField.STRING, self.subgraph.Swap.tokenOut.id, "uknown")

        # left inner joins between swaps and pools
        self.subgraph.Swap.pool_name = SyntheticField.map(pool_name_dict, SyntheticField.STRING, self.subgraph.Swap.pool.id, "uknown")
        self.subgraph.Swap.pool_symbol = SyntheticField.map(pool_symbol_dict, SyntheticField.STRING, self.subgraph.Swap.pool.id, "uknown")
        #################################################################################################################


        # define query search params based off of filter_dict
        swaps_qp = self.subgraph.Query.swaps(
            first=query_size,
            orderBy=self.subgraph.Query.swaps.timestamp,
            orderDirection='desc',
            where = filter_dict
        )

        matched_query_path = match_query_paths(query_paths=query_paths, default_query_path = swaps_qp)
        return self.query(
                    query_path=matched_query_path,
                    saved_file_name=saved_file_name,
                    add_endpoint_col=add_endpoint_col
                )

        