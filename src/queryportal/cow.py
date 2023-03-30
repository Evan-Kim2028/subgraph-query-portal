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
class Cow:
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
    def query_trades(
            self,
            query_size: int = None,
            filter_dict: dict = {},
            save_data: bool = False,
            token_names: bool = True,       # currently unused
            saved_file_name: str = None,
            add_endpoint_col: bool = True
            ) -> pl.DataFrame:
        """
        Parameters:
        query_trades() queries a DEX trades schema from a Subgraph GraphQL endpiont. It returns a Polars DataFrame of Trade data that is the equivalent to a materialized view with SQL tables.
        """
        # define subgraph Trade entity
        trades_entity = self.subgraph.Trade
        # insert datetime synthetic field
        trades_entity.datetime = SyntheticField.datetime_of_timestamp(self.subgraph.Trade.timestamp)
        # DEBUG - confirms synthetic field wasa dded to the entity
        # print(list((field.name, TypeRef.graphql(field.type_)) for field in trades_entity._object.fields))
        # print('DEBUG')

        if add_endpoint_col:
            trades_entity.endpoint = synthetic_endpoint(self.endpoint)

        # use synthetic field to change Trade values to float
        trades_entity.sellAmount_float = SyntheticField(
                f=lambda value: float(value),
                type_=SyntheticField.FLOAT,
                deps=trades_entity.sellAmount,
            )
        trades_entity.buyAmount = SyntheticField(
                f=lambda value: float(value),
                type_=SyntheticField.FLOAT,
                deps=trades_entity.buyAmount,
            )
        
        trades_entity.gasPrice = SyntheticField(
                f=lambda value: float(value),
                type_=SyntheticField.FLOAT,
                deps=trades_entity.gasPrice,
            )

        trades_entity.feeAmount = SyntheticField(
                f=lambda value: float(value),
                type_=SyntheticField.FLOAT,
                deps=trades_entity.feeAmount,
            )


        # define query search params based off of param_dict
        trades_qp = self.subgraph.Query.trades(
            first=query_size,
            orderBy=self.subgraph.Query.trades.timestamp,
            orderDirection='desc',
            where = filter_dict
        )

        # run query
        df = self.sg.query_df(trades_qp)

        # drop redundant cols
        df = df.drop(columns=['trades_buyAmount', 'trades_sellAmount', 'trades_feeAmount', 'trades_gasPrice'])

        # convert df to polars DataFrame
        trades_df = pl.from_pandas(df)

        if save_data:
            # check if data folder exists. If it doesn't, create it
            if not os.path.exists('data'):
                os.makedirs('data')
            if saved_file_name:
                trades_df.write_parquet(f'data/{saved_file_name}.parquet')
            else:
                trades_df.write_parquet(f'data/{endpoint_name(self.endpoint)}.parquet')
                
        return trades_df