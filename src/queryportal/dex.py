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
    # load Subgrounds object
    subgraph: Subgraph = None
    sg = Subgrounds()

    def __post_init__(self):
        # load dex subgraph schema information from the the subgraph endpoint. This is represented as a Subgraph object.
        self.subgraph = self.sg.load(self.endpoint)

    @timeit
    @df_describe
    def query_swaps(
            self,
            query_size: int = None,
            filter_dict: dict = {},
            save_data: bool = False,
            token_names: bool = True,
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
        # DEBUG - confirms synthetic field wasa dded to the entity
        # print(list((field.name, TypeRef.graphql(field.type_)) for field in swaps_entity._object.fields))
        # print('DEBUG')

        if add_endpoint_col:
            swaps_entity.endpoint = synthetic_endpoint(self.endpoint)

        # use synthetic field to change swap values to float
        swaps_entity.amountOut_float = SyntheticField(
                f=lambda value: float(value),
                type_=SyntheticField.FLOAT,
                deps=swaps_entity.amountOut,
            )
        swaps_entity.amountIn_float = SyntheticField(
                f=lambda value: float(value),
                type_=SyntheticField.FLOAT,
                deps=swaps_entity.amountIn,
            )
        if token_names: # if it's true, do a synthetic merge to add token names automatically to the swaps df
            # run token query
            token_df = self.query_tokens(
                query_size=2500,
                save_data=True,
                add_endpoint_col=True
                )

            # create a dictionary of token ids and their symbols
            token_dict = dict(zip(token_df['tokens_id'], token_df['tokens_symbol']))

            # add symbol synthetic field to the Swap entity
            swaps_entity.symbol = SyntheticField(
                f=lambda value: token_dict[value],
                type_=SyntheticField.STRING,
                deps=swaps_entity.token_id,
            )
        


        # define query search params based off of param_dict
        swaps_qp = self.subgraph.Query.swaps(
            first=query_size,
            orderBy=self.subgraph.Query.swaps.timestamp,
            orderDirection='desc',
            where = filter_dict
        )

        # run query
        df = self.sg.query_df(swaps_qp)

        # drop amountIn and amountOut cols
        df = df.drop(columns=['swaps_amountIn', 'swaps_amountOut'])

        # convert df to polars DataFrame
        swaps_df = pl.from_pandas(df)

        if save_data:
            # check if data folder exists. If it doesn't, create it
            if not os.path.exists('data'):
                os.makedirs('data')
            if saved_file_name:
                swaps_df.write_parquet(f'data/{saved_file_name}.parquet')
            else:
                swaps_df.write_parquet(f'data/{endpoint_name(self.endpoint)}.parquet')
                
        return swaps_df


    @timeit
    @df_describe
    def query_tokens(
            self, 
            query_size: int,
            filter_dict: dict = {},
            save_data=None, 
            saved_file_name: str = None,
            add_endpoint_col: bool = True
            ) -> pl.DataFrame:
        """
        Runs a query against the tokens schema to get token names
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

        # convert df to polars
        tokens_df = pl.from_pandas(df)


        if save_data:
            # check if data folder exists. If it doesn't, create it
            if not os.path.exists('data'):
                os.makedirs('data')
            if saved_file_name:
                tokens_df.write_parquet(f'data/{saved_file_name}.parquet')
            else:
                tokens_df.write_parquet(f'data/{endpoint_name(self.endpoint)}.parquet')

        return tokens_df

