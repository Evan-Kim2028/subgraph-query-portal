import polars as pl

from dataclasses import dataclass
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
    sg = Subgrounds()

    def __post_init__(self):
        # load dex subgraph schema information from the the subgraph endpoint. This is represented as a Subgraph object.
        self.subgraph = self.sg.load(self.endpoint)

    def query(
            self, 
            entity,
            query_path,
            saved_file_name: str = None,
            add_endpoint_col: bool = True
            ) -> pl.DataFrame:
        """
        Concrete implementation of the abstract query method. Requires entity and query_path as inputs.
        """
        if add_endpoint_col:
            entity.endpoint = synthetic_endpoint(self.endpoint)

        # obtain pandas dataframe of query results
        df = self.sg.query_df(query_path)

        converted_df = to_polars(df)

        if saved_file_name is not None:
            save_file(converted_df, saved_file_name)

        return converted_df
    
    @timeit
    @df_describe
    def query_swaps(self, query_size=5, filter_dict={}, saved_file_name=None, add_endpoint_col=True) -> pl.DataFrame:
        """
        This method allows query construction from the Swap entity. It takes in query parameters as inputs and returns a 
        Polars DataFrame of the query results. The method also adds a datetime column to the swaps entity by converting the 
        timestamp column to datetime format using a synthetic field. The `add_endpoint_col` parameter is used to add the 
        endpoint column to the query results if set to True.
        """
        # define subgraph swap entity
        swaps_entity = self.subgraph.Swap

        # define query search params based off of filter_dict
        swaps_qp = self.subgraph.Query.swaps(
            first=query_size,
            orderBy=self.subgraph.Query.swaps.timestamp,
            orderDirection='desc',
            where = filter_dict
        )

        # swaps entity has a timestamp integer column. We convert that to datetime format using a synthetic field.
        swaps_entity.datetime = SyntheticField.datetime_of_timestamp(swaps_entity.timestamp)

        # call the abstract query method with explicit arguments
        return self.query(
            entity=swaps_entity, 
            query_path=swaps_qp,
            saved_file_name=saved_file_name, 
            add_endpoint_col=add_endpoint_col
        )
    
    @timeit
    @df_describe
    def query_tokens(self, query_size=5, filter_dict={}, saved_file_name=None, add_endpoint_col=True) -> pl.DataFrame:
        """
        Runs a query against the tokens schema
        """
        # define subgraph swap entity
        tokens_entity = self.subgraph.Token

        # define query search params based off of filter_dict
        tokens_qp = self.subgraph.Query.tokens(
            first=query_size,
            where = filter_dict
        )

        # call the abstract query method with explicit arguments
        return self.query(
            entity=tokens_entity, 
            query_path=tokens_qp,
            saved_file_name=saved_file_name, 
            add_endpoint_col=add_endpoint_col
        )

    @timeit
    @df_describe
    def query_pools(self, query_size=5, filter_dict={}, saved_file_name=None, add_endpoint_col=True) -> pl.DataFrame:
        """
        Runs a query against the liquiditypools entity
        """

        # define subgraph swap entity
        pools_entity = self.subgraph.LiquidityPool
        
        # define query search params based off of filter_dict
        pools_qp = self.subgraph.Query.liquidityPools(
            first=query_size,
            where = filter_dict
        )

        # call the abstract query method with explicit arguments
        return self.query(
            entity=pools_entity, 
            query_path=pools_qp,
            saved_file_name=saved_file_name, 
            add_endpoint_col=add_endpoint_col
        )
    
    @timeit
    @df_describe
    def query_firehose(self, query_size=5, filter_dict={}, saved_file_name=None, add_endpoint_col=True) -> pl.DataFrame:
        """
        Runs a query against the firehose entity
        """

        # 1. run token and pools query to get id info for joining
        token_df = self.query_tokens(query_size = 100000)

        pool_df = self.query_pools(query_size = 100000)

        # create a dictionary of token ids and their symbols
        token_symbol_dict = dict(zip(token_df['tokens_id'], token_df['tokens_symbol']))
        token_decimal_dict = dict(zip(token_df['tokens_id'], token_df['tokens_decimals']))

        # create a dictionary of pool ids and their tokens
        pool_name_dict = dict(zip(pool_df['liquidityPools_id'], pool_df['liquidityPools_name']))
        pool_symbol_dict = dict(zip(pool_df['liquidityPools_id'], pool_df['liquidityPools_symbol']))

        # define subgraph swap entity
        swaps_entity = self.subgraph.Swap

        # define query search params based off of filter_dict
        swaps_qp = self.subgraph.Query.swaps(
            first=query_size,
            orderBy=self.subgraph.Query.swaps.timestamp,
            orderDirection='desc',
            where = filter_dict
        )


        # insert datetime synthetic field
        swaps_entity.datetime = SyntheticField.datetime_of_timestamp(swaps_entity.timestamp)

        # left inner joins between swaps and tokens
        swaps_entity.tokenIn_symbol = SyntheticField.map(token_symbol_dict, SyntheticField.STRING, swaps_entity.tokenIn.id, "uknown")
        swaps_entity.tokenOut_symbol = SyntheticField.map(token_symbol_dict, SyntheticField.STRING, swaps_entity.tokenOut.id, "uknown")
        swaps_entity.tokenIn_decimals = SyntheticField.map(token_decimal_dict, SyntheticField.INT, swaps_entity.tokenIn.id, 0)
        swaps_entity.tokenOut_decimals = SyntheticField.map(token_decimal_dict, SyntheticField.INT, swaps_entity.tokenOut.id, 0)

        # left inner joins between swaps and pools
        swaps_entity.pool_name = SyntheticField.map(pool_name_dict, SyntheticField.STRING, swaps_entity.pool.id, "uknown")
        swaps_entity.pool_symbol = SyntheticField.map(pool_symbol_dict, SyntheticField.STRING, swaps_entity.pool.id, "uknown")

        # call the abstract query method with explicit arguments
        return self.query(
            entity=swaps_entity, 
            query_path=swaps_qp,
            saved_file_name=saved_file_name, 
            add_endpoint_col=add_endpoint_col
        )