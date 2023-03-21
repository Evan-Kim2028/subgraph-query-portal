import os
import polars as pl

from dataclasses import dataclass
from datetime import datetime
from subgrounds import Subgrounds
from queryportal.benchmark import Benchmark
from queryportal.queryfilter import QueryFilter

@dataclass
class Dex:
    """
    DEX class stores standardized Messari DEX query methods for easier access. 
    The queries assume that Messari schemas and may not function properly if used with non-Messari standardized Dex subgraphs.
    """
    endpoint: str
    # load Subgrounds object
    sg = Subgrounds()


    @Benchmark.timeit
    @Benchmark.df_describe
    def query_swaps(
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
        token_in: list[str] - list of token_in addresses to query
        token_out: list[str] - list of token_out addresses to query
        query_size: int - number of swaps to query
        save_data: bool - whether to save the data to a parquet file. Default = False
        saved_file_name: str - if non-empty, use custom file name. If None, default endpoint name.
        add_endpoint_col: bool - whether to add a column to the dataframe with the endpoint url name. Default = True
        
        query_swap_data() queries a DEX swaps schema from a Subgraph endpiont. It returns a Polars DataFrame of swap data.

        TODO - add automatic token_name query so you can query based off of token symbol instead of token address

        """

        # load dex subgraph schema information from the the subgraph endpoint
        dex_schema = self.sg.load_subgraph(self.endpoint)
        # define field path
        swaps_fp = dex_schema.Query.swaps

        # instantiate QueryFilter object # TODO - come up with cleaner implementation. Maybe ENUM?
        query_filter = QueryFilter()

        # call query_tokens() to get addresses of token names.
        if token_in != None:
            token_in_df = self.query_tokens(ticker_list=token_in)
            token_in_df = token_in_df.rename(
                {
                'tokens_id': 'swaps_tokenIn_id',
                'tokens_name': 'swaps_tokenIn_name',
                'tokens_symbol': 'swaps_tokenIn_symbol',
                'tokens_decimals': 'swaps_tokenIn_decimals',
                'tokens_lastPriceUSD': 'swaps_tokenIn_lastPriceUSD'
                 }
                )
            token_in = token_in_df['swaps_tokenIn_id'].to_list()
        else:
            token_in = None
            token_in_df = None

        if token_out != None:
            token_out_df = self.query_tokens(ticker_list=token_out)
            # change column name
            token_out_df = token_out_df.rename(
                {'tokens_id': 'swaps_tokenOut_id',
                'tokens_name': 'swaps_tokenOut_name',
                'tokens_symbol': 'swaps_tokenOut_symbol',
                'tokens_decimals': 'swaps_tokenOut_decimals',
                'tokens_lastPriceUSD': 'swaps_tokenOut_lastPriceUSD'
                 }
                )
            token_out = token_out_df['swaps_tokenOut_id'].to_list()
        else:
            token_out = None
            token_out_df = None

        # construct query filter dict
        param_dict = query_filter.make_search_param(start_time, end_time, token_in, token_out)

        # define query search params based off of param_dict
        swaps_qp = swaps_fp(
            first=query_size,
            orderBy='timestamp',
            orderDirection='desc',
            where = param_dict
        )

        # run query
        df = self.sg.query_df(swaps_qp)

        # convert swaps_amountOut and swaps_amountIn to floats
        df['swaps_amountOut'] = df['swaps_amountOut'].astype(float)
        df['swaps_amountIn'] = df['swaps_amountIn'].astype(float)

        if add_endpoint_col:
            # add endpoint column
            name = self.endpoint.split('/')[-1]
            df['endpoint'] = name

        # convert df to polars DataFrame
        swaps_df = pl.from_pandas(df)

        # join and replace token addresses with token names
        if not token_in == None:
            swaps_df = swaps_df.join(token_in_df, on='swaps_tokenIn_id', how='inner')
            print('merged token_in_df')    
        if not token_out == None:
            swaps_df = swaps_df.join(token_out_df, on='swaps_tokenOut_id', how='inner')
            print('merged token_out_df')

        if save_data:
            # check if data folder exists. If it doesn't, create it
            if not os.path.exists('data'):
                os.makedirs('data')
            if saved_file_name:
                swaps_df.write_parquet(f'data/{saved_file_name}.parquet')
            else:
                swaps_df.write_parquet(f'data/{name}.parquet')
                
        return swaps_df


    @Benchmark.timeit
    @Benchmark.df_describe
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
        if ticker_list != None:
            # load dex subgraph schema information from the the subgraph endpoint
            token_schema = self.sg.load_subgraph(self.endpoint)

            # define field path
            tokens_fp = token_schema.Query.tokens

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

            if add_endpoint_col:
                # add endpoint column
                name = self.endpoint.split('/')[-1]
                df['endpoint'] = name

            if save_data:
                # check if data folder exists. If it doesn't, create it
                if not os.path.exists('data'):
                    os.makedirs('data')
                if saved_file_name:
                    tokens_df.write_parquet(f'data/{saved_file_name}.parquet')
                else:
                    tokens_df.write_parquet(f'data/{name}.parquet')

            return tokens_df
        else:
            return None


    def date_to_time(self, dt: datetime) -> int:
        """
        date_to_time() converts a datetime object to a timestamp
        TODO - 3/18/23 - Do I add helper functions to convert between datetime and timestamp?
        """
        return int(round(dt.timestamp()))
    