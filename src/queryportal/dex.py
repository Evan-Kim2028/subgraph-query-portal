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
    dex_subgraph: Subgraph = None
    sg = Subgrounds()

    def __post_init__(self):
        # load dex subgraph schema information from the the subgraph endpoint. This is represented as a Subgraph object.
        self.dex_subgraph = self.sg.load(self.endpoint)



    @timeit
    @df_describe
    def query_swaps(
            self,
            query_size: int = None,
            filter_dict: dict = {},
            save_data: bool = False,
            saved_file_name: str = None,
            add_endpoint_col: bool = True
            ) -> pl.DataFrame:
        """
        Parameters:
        start_time: int - unix timestamp of the start time of the query range
        end_time: int - unix timestamp of the end time of the query range
        token_in: list[str] - list of token_in addresses to query
        token_out: list[str] - list of token_out addresses to query
        query_size: int - number of swaps to query
        save_data: bool - whether to save the data to a parquet file. Default = False
        saved_file_name: str - if non-empty, use custom file name. If None, default endpoint name.
        add_endpoint_col: bool - whether to add a column to the dataframe with the endpoint url name. Default = True
        
        query_swap_data() queries a DEX swaps schema from a Subgraph endpiont. It returns a Polars DataFrame of swap data.

        TODO - add automatic token_name query so you can query based off of token symbol instead of token address

        """
        # define subgraph swap entity
        swaps_entity = self.dex_subgraph.Swap
        # insert datetime synthetic field
        swaps_entity.datetime = SyntheticField.datetime_of_timestamp(self.dex_subgraph.Swap.timestamp)
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

        # define query search params based off of param_dict
        swaps_qp = self.dex_subgraph.Query.swaps(
            first=query_size,
            orderBy=self.dex_subgraph.Query.swaps.timestamp,
            orderDirection='desc',
            where = filter_dict
        )

        # run query
        df = self.sg.query_df(swaps_qp)

        # drop amountIn and amountOut cols
        df = df.drop(columns=['swaps_amountIn', 'swaps_amountOut'])

        # convert df to polars DataFrame
        swaps_df = pl.from_pandas(df)
        ########################################################

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
            # names_list: list[str] = None, 
            ticker_list: list[str] = None,
            save_data=None, 
            saved_file_name: str = None,
            add_endpoint_col: bool = True
            ) -> pl.DataFrame:
        """
        Runs a query against the tokens schema to get token names
        """
        # define subgraph swap entity
        tokens_entity = self.dex_subgraph.Token

        if ticker_list != None:
            # define field path
            tokens_fp = self.dex_subgraph.Query.tokens

            if add_endpoint_col:
                tokens_entity.endpoint = synthetic_endpoint(self.endpoint)

            tokens_qp = tokens_fp(
                # first=100000, # hardcode arbitrary large number to trigger query pagination automaticaly if needed.
                # orderBy='symbol',
                # orderDirection='desc',
                where = {
                'symbol_in' : ticker_list, # TODO  3/20/23 - Create dynamic field search param dictionary
                # 'name_in' : names_list,
                'lastPriceUSD_gt': 0
                }
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
        else:
            return None
