from queryportal.new_dex import Dex

import polars as pl
pl.Config.set_fmt_str_lengths(200)

dex_endpoints = [
    'https://api.thegraph.com/subgraphs/name/messari/uniswap-v3-ethereum',
    'https://api.thegraph.com/subgraphs/name/messari/uniswap-v3-arbitrum',
    'https://api.thegraph.com/subgraphs/name/messari/uniswap-v3-polygon',
    'https://api.thegraph.com/subgraphs/name/messari/uniswap-v3-optimism',
]

# instantiate Dex class with subgraph key
dex = Dex(endpoints=dex_endpoints)

query_paths = [
    'hash',
    'pool_name', 
    # 'pool_inputTokens_name', #This is a nested struct. Although there is logic to handle a single struct, it is not yet implemented for nested structs. Not sure if it should be either.
    'tokenIn_symbol', 
    'tokenOut_symbol', 
    'amountOutUSD', 
    'amountInUSD',
    'amountOut',
    'amountIn',
    ]

for subgraph_name in list(dex.subject.subgraphs.keys()):
    df = dex.query_swaps(
    subgraph_name=subgraph_name, 
    query_paths=query_paths,
    filter_dict = {'tokenIn_symbol': 'WETH', 'amountOutUSD_lt': .001}
    )

    print(df.head(5))


# # AFTER
# df = dex.query(
#     entity='swaps',
#     orderBy='timestamp',
#     subgraph_name=subgraph_name, 
#     query_paths=query_paths,
#     filter_dict = {'tokenIn_symbol': 'WETH', 'amountOutUSD_lt': .001}
#     )
# # TYPE OUTPUT - 

# df = dex.query(
#     entity='tokens',
#     orderBy='symbol',
#     subgraph_name=subgraph_name, 
#     query_paths=query_paths,
#     filter_dict = {'tokenIn_symbol': 'WETH', 'amountOutUSD_lt': .001}
#     )



# NOTES
# pre-query schema info, polars lazy eval I think works






print('done')