import os
import polars as pl

from dataclasses import dataclass
from datetime import datetime
from subgrounds import Subgrounds
from queryportal.benchmark import Benchmark
from queryportal.queryfilter import QueryFilter

@dataclass
class Dex:
    endpoint: str

    @Benchmark.timeit
    @Benchmark.df_describe
    def query_swap_data(
            self,
            start_time: int = None, 
            end_time: int = None, 
            token_in: list[str] = None,
            token_out: list[str] = None,
            query_size: int = None,
            save_data: bool = False,
            saved_file_name: str = None,
            add_endpoint_col: bool = True
            ) -> pl.DataFrame:
        """
        Parameters:
        start_time: int - unix timestamp of the start time of the query range
        end_time: int - unix timestamp of the end time of the query range
        query_size: int - number of swaps to query
        save_data: bool - whether to save the data to a parquet file. Default = False
        saved_file_name: str - if non-empty, use custom file name. If None, default endpoint name.
        add_endpoint_col: bool - whether to add a column to the dataframe with the endpoint url name. Default = True
        
        query_swap_data() queries a DEX swaps schema from a Subgraph endpiont. It returns a Polars DataFrame of swap data.
        Returns a Polars DataFrame of swap data.

        
        TODO - to use token_in and token_out, need to construct a field path from the ground up specify which query parameters to use. Currently it's all or none approach and it's too rigid


        """
        # load Subgrounds object
        sg = Subgrounds()
        # load dex subgraph schema information from the the subgraph endpoint
        dex_schema = sg.load_subgraph(self.endpoint)
        # define field path
        swaps_fp = dex_schema.Query.swaps

        # instantiate QueryFilter object # TODO - come up with cleaner implementation. Maybe ENUM?
        query_filter = QueryFilter()
        # construct query filter dict
        param_dict = query_filter.make_search_param(start_time, end_time, token_in, token_out)
        print(f'DEBUGGING: param_dict = {param_dict}')
        swaps_qp = swaps_fp(
            first=query_size,
            orderBy='timestamp',
            orderDirection='desc',
            where = param_dict
        )

        # run query
        df = sg.query_df(swaps_qp)

        # convert swaps_amountOut and swaps_amountIn to floats
        df['swaps_amountOut'] = df['swaps_amountOut'].astype(float)
        df['swaps_amountIn'] = df['swaps_amountIn'].astype(float)


        if add_endpoint_col:
            # add endpoint column
            name = self.endpoint.split('/')[-1]
            df['endpoint'] = name

        # convert df to polars DataFrame
        swaps_df = pl.from_pandas(df)

        if save_data:
            # check if data folder exists. If it doesn't, create it
            if not os.path.exists('data'):
                os.makedirs('data')
            if saved_file_name:
                swaps_df.write_parquet(f'data/{saved_file_name}.parquet')
            else:
                swaps_df.write_parquet(f'data/{name}.parquet')
                
        return swaps_df

    def date_to_time(self, dt: datetime) -> int:
        """
        date_to_time() converts a datetime object to a timestamp
        TODO - 3/18/23 - Do I add helper functions to convert between datetime and timestamp?
        """
        return int(round(dt.timestamp()))
    