from queryportal.dex import Dex
from datetime import datetime, timedelta

# define subgraph endpoint. This one is the Univ3 Ethereum endpoint maintained by Messari
endpoint = 'https://api.thegraph.com/subgraphs/name/messari/uniswap-v3-ethereum'

# instantiate dex class. Dex stores dex-related query functions
my_dex = Dex(endpoint)

#####################################################
# Test functionality of query with filter dict
#
#####################################################
filter_dict = {
    'timestamp_gte': int((datetime.today() - timedelta(days=1)).timestamp()),
    'timestamp_lte': int(datetime.today().timestamp()),
    'tokenIn_':  {'symbol_in': ['OHM', 'GOHM']},
}

query_paths = [
    'timestamp', 
    'pool_name', 
    # 'pool_inputTokens_name', # this returns an array of values which doubles amount of rows...
    'tokenIn_symbol', 
    'tokenOut_symbol', 
    'amountOutUSD', 
    'amountInUSD']

my_dex.query_swaps(
    query_paths = query_paths,
    query_size = 500,
    filter_dict = filter_dict, 
    saved_file_name='nested_filter'
    )