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
## NEW
filter_dict = {
    # 'timestamp_gte': int((datetime.today() - timedelta(days=1)).timestamp()),
    # 'timestamp_lte': int(datetime.today().timestamp()),
    'pool_name': 'Uniswap V3 Pepe/Wrapped Ether 1%'
}

query_cols = [
    # 'timestamp', 
    # 'hash',
    'datetime', #synthetic field
    'pool_name', 
    # 'pool_inputTokens_name', # this returns an array of values which doubles amount of rows due to flattening logic in Subgrounds
    'tokenIn_symbol', 
    'tokenOut_symbol', 
    # 'amountOutUSD', 
    # 'amountInUSD',
    # 'amountOut',
    # 'amountIn',
    ]

df = my_dex.query_swaps(query_paths=query_cols, filter_dict=filter_dict, query_size=100, add_endpoint_col=False)

print(df)