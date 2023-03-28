import os
import polars as pl

from dataclasses import dataclass
from datetime import datetime
from subgrounds import Subgrounds, Subgraph
from subgrounds.subgraph import SyntheticField
from queryportal.benchmark import Benchmark

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

        # define subgraph swap entity
        swaps_entity = self.dex_subgraph.Swap
        # insert datetime synthetic field
        swaps_entity.datetime = SyntheticField.datetime_of_timestamp(self.dex_subgraph.Swap.timestamp)
        # DEBUG - confirms synthetic field wasa dded to the entity
        # print(list((field.name, TypeRef.graphql(field.type_)) for field in swaps_entity._object.fields))
        # print('DEBUG')

        # convert start_time and end_time to datetime objects
        if start_time != None:
            start_time = self.date_to_time(start_time)
        if end_time != None:
            end_time = self.date_to_time(end_time)

        #######################################################################################
        # this logic is to execute pre-query on tokens to get the name of the tokena addresses.
        # instantiate QueryFilter object 
        # TODO - come up with cleaner implementation. Maybe ENUM?
        # query_filter = QueryFilter()

        # call query_tokens() to get addresses of token names. This logic is required because there is a single token list but swaps has two token columns (token_in and token_out)
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
        #######################################################################################




        ########################################################
        # this logic is to construct and execute the swaps query

        # construct query filter dict
        param_dict = self.make_search_param(start_time, end_time, token_in, token_out)

        # define query search params based off of param_dict
        swaps_qp = self.dex_subgraph.Query.swaps(
            first=query_size,
            orderBy=self.dex_subgraph.Query.swaps.timestamp,
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
        ########################################################


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
            # define field path
            tokens_fp = self.dex_subgraph.Query.tokens

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

    @staticmethod
    def date_to_time(dt: datetime) -> int:
        """
        date_to_time() converts a datetime object to a timestamp
        """
        return int(round(dt.timestamp()))
    

    def make_search_param(
            self,             
            start_time: int = None, 
            end_time: int = None, 
            token_in: list[str] = None,
            token_out: list[str] = None,
            ) -> dict:
        """
        make_search_param constructs a search parameter query. This is used upstream to get passed into the
        query_swap function. The filter parameters are specified based off of the search_param dictionary keys.
        """
        
        # empty query dict that will be filled up and returned.
        search_query_dict = {}

        # check variable type. For any None type, do not add to query dictionary
        if self.check_type(start_time) is not None:
            search_query_dict['timestamp_gte'] = start_time
        if self.check_type(end_time) is not None:
            search_query_dict['timestamp_lt'] = end_time
        if self.check_type(token_in) is not None:
            search_query_dict['tokenIn_in'] = token_in
        if self.check_type(token_out) is not None:
            search_query_dict['tokenOut_in'] = token_out

        return search_query_dict
        
    def check_type(self, variable):
        """
        Helper function checks the variable type. If the variable type is None, return None
        """
        match variable:
            case int():
                return variable
            case list():
                for element in variable:
                    if not isinstance(element, str):
                        print(f'Type Mismatch: {element} is {type(element)} and needs to contain all strings. However it contains {element}, which is type {type(element)}, which is not a string. Return None')
                        return None
                return variable            
            case Other:
                print(f'Type Mismatch: {variable} is {type(variable)}. Return None')
                return None
