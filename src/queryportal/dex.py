import os
import polars as pl

from dataclasses import dataclass
from datetime import datetime
from subgrounds import Subgrounds
from subgrounds.schema import TypeRef
from subgrounds.subgraph import Subgraph
from subgrounds.subgraph import SyntheticField
from queryportal.helpers import *

@dataclass
class Dex:
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


    @timeit
    @df_describe
    def query_swaps(
            self,
            query_size: int = 5,
            filter_dict: dict = {},
            save_data: bool = False,
            saved_file_name: str = None,
            add_endpoint_col: bool = True
            ) -> pl.DataFrame:
        """
        Parameters:
        query_swaps() queries a DEX swaps schema from a Subgraph GraphQL endpiont. It returns a Polars DataFrame of swap data that is the equivalent to a materialized view with SQL tables.
        """
        # define subgraph swap entity
        swaps_entity = self.subgraph.Swap
        # insert datetime synthetic field
        swaps_entity.datetime = SyntheticField.datetime_of_timestamp(swaps_entity.timestamp)

        if add_endpoint_col:
            swaps_entity.endpoint = synthetic_endpoint(self.endpoint)

        # run token query
        token_df = self.query_tokens(
            query_size=10000,
            add_endpoint_col=True
            )

        # create a dictionary of token ids and their symbols
        token_symbol_dict = dict(zip(token_df['tokens_id'], token_df['tokens_symbol']))
        token_decimal_dict = dict(zip(token_df['tokens_id'], token_df['tokens_decimals']))

        # left inner joins between swaps and tokens
        swaps_entity.tokenIn_symbol = SyntheticField.map(token_symbol_dict, SyntheticField.STRING, swaps_entity.tokenIn.id, "uknown")
        swaps_entity.tokenOut_symbol = SyntheticField.map(token_symbol_dict, SyntheticField.STRING, swaps_entity.tokenOut.id, "uknown")
        swaps_entity.tokenIn_decimals = SyntheticField.map(token_decimal_dict, SyntheticField.INT, swaps_entity.tokenIn.id, 0)
        swaps_entity.tokenOut_decimals = SyntheticField.map(token_decimal_dict, SyntheticField.INT, swaps_entity.tokenOut.id, 0)

        # check if fieldpath exists. If it does, do synthetic convert. TODO - refactor this code
        try:
            swaps_entity.amountIn_float = synthetic_convert(type=SyntheticField.FLOAT, deps=swaps_entity.amountIn)
        except KeyError:
            pass

        try:
            swaps_entity.amountOut_float = synthetic_convert(type=SyntheticField.FLOAT, deps=swaps_entity.amountOut)
        except KeyError:
            pass

        try:
            swaps_entity.gasLimit_float = synthetic_convert(type=SyntheticField.FLOAT, deps=swaps_entity.gasLimit)
        except KeyError:
            pass

        try:
            swaps_entity.gasPrice_float = synthetic_convert(type=SyntheticField.FLOAT, deps=swaps_entity.gasPrice)
        except KeyError:
            pass

        try:
            swaps_entity.gasUsed_float = synthetic_convert(type=SyntheticField.FLOAT, deps=swaps_entity.gasUsed)
        except KeyError:
            pass

        try:
            swaps_entity.nonce_float = synthetic_convert(type=SyntheticField.FLOAT, deps=swaps_entity.nonce)
        except KeyError:
            pass

        try:
            swaps_entity.tick_float = synthetic_convert(type=SyntheticField.FLOAT, deps=swaps_entity.tick)
        except KeyError:
            pass

        # MIGHT USE THIS CODE LATER
        # if hasattr(swaps_entity, 'amountIn'):
        #     print('has attribute!')
        # else:
        #     pass


        # define query search params based off of param_dict
        swaps_qp = self.subgraph.Query.swaps(
            first=query_size,
            orderBy=self.subgraph.Query.swaps.timestamp,
            orderDirection='desc',
            where = filter_dict
        )

        # run query
        df = self.sg.query_df(swaps_qp)

        drop_cols = ['swaps_amountIn', 'swaps_amountOut', 'swaps_gasLimit', 'swaps_gasPrice', 'swaps_tick', 'swaps_nonce', 'swaps_gasUsed']
        # check if columns exist:
        for col in drop_cols:
            if col in df.columns.to_list():  # if column exists, then drop it
                df.drop(col, axis=1, inplace=True)

        # print what types each swaps_df is
        # convert swaps_df to polars DataFrame
        swaps_df = pl.from_pandas(df)
        
        # save df to parquet
        if save_data is not None:
            save_file(swaps_df, saved_file_name)
                
        return swaps_df


    @timeit
    @df_describe
    def query_tokens(
            self, 
            query_size: int = 5,
            filter_dict: dict = {},
            saved_file_name: str = None,
            add_endpoint_col: bool = True
            ) -> pl.DataFrame:
        """
        Runs a query against the tokens schema
        """
        # define subgraph swap entity
        tokens_entity = self.subgraph.Token

        tokens_fp = self.subgraph.Query.tokens

        if add_endpoint_col:
            tokens_entity.endpoint = synthetic_endpoint(self.endpoint)

        tokens_qp = tokens_fp(
            first=query_size,
            where = filter_dict
        )

        df = self.sg.query_df(tokens_qp)
        
        # drop these columns - 3/31/23 - not sure where they are coming from but they don't appear to populate in all tokens dex schemas
        non_standard_token_cols = ['tokens__totalSupply', 'tokens__totalValueLockedUSD', 'tokens__largePriceChangeBuffer', 'tokens__largeTVLImpactBuffer']
        # check if columns exist:
        for col in non_standard_token_cols:
            if col in df.columns.to_list():  # if column exists, then drop it
                df.drop(col, axis=1, inplace=True)

        # convert df to polars
        tokens_df = pl.from_pandas(df)

        if saved_file_name is not None:
            save_file(tokens_df, saved_file_name)

        return tokens_df

    @timeit
    @df_describe
    def query_liquiditypools(
            self, 
            query_size: int = 5,
            filter_dict: dict = {},
            saved_file_name: str = None,
            add_endpoint_col: bool = True
            ) -> pl.DataFrame:
        """
        Runs a query against the liquiditypools entity
        """

        # define subgraph swap entity
        liquidityPool_entity = self.subgraph.LiquidityPool

        liquidityPools_fp = self.subgraph.Query.liquidityPools

        if add_endpoint_col:
            liquidityPool_entity.endpoint = synthetic_endpoint(self.endpoint)

        liquidityPools_qp = liquidityPools_fp(
            first=query_size,
            where = filter_dict
        )

        # obtain pandas dataframe of query results
        df = self.sg.query_df(liquidityPools_qp)

        converted_df = to_polars(df)

        if saved_file_name is not None:
            save_file(converted_df, saved_file_name)

        return converted_df



