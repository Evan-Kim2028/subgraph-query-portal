import polars as pl

from datastreams.datastream import Streamer
from dataclasses import dataclass
from datetime import datetime
from usdc_depeg.benchmark import Benchmark

@dataclass
class Dex:
    endpoint: str

    @Benchmark.timeit
    @Benchmark.df_describe
    def query_swap_data(
            self,
            start_time: int, 
            end_time: int, 
            # token_in: list[str],
            # token_out: list[str],
            query_size: int
            ) -> pl.DataFrame:
        """
        get_swap_data() hardcodes logic to preprocess swap data from a dex subgraph using DataStreams
        
        Returns a list of pool ID addresses.
        """
        streamer = Streamer(self.endpoint)

        # define field path
        swaps_fp = streamer.queryDict.get('swaps')
        
        # define query path from the field path
        swaps_qp = swaps_fp(
            first=query_size,
            orderBy='timestamp',
            orderDirection='desc',
            where = {
            'timestamp_gte': start_time,
            'timestamp_lt': end_time
            # 'tokenIn_id_in': token_in,
            # 'tokenOut_id_in': token_out
            }
        )

        # run query
        df = streamer.runQuery(swaps_qp)

        # convert swaps_amountOut and swaps_amountIn to floats
        df['swaps_amountOut'] = df['swaps_amountOut'].astype(float)
        df['swaps_amountIn'] = df['swaps_amountIn'].astype(float)

        # convert df to polars DataFrame
        swaps_df = pl.from_pandas(df)

        return swaps_df

    def datetime_to_timestamp(self, dt: datetime) -> int:
        """
        datetime_to_timestamp() converts a datetime object to a timestamp
        """

        return int(round(dt.timestamp()))
    