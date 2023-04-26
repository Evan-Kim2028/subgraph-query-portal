from queryportal.new_dex import Dex

import polars as pl
pl.Config.set_fmt_str_lengths(200)


# instantiate Dex class with subgraph key
dex = Dex(endpoints='https://api.thegraph.com/subgraphs/name/messari/uniswap-v3-ethereum')

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

df = dex.generic_query(
    entity='swaps',
    # orderBy='symbol',
    subgraph_name='uniswap-v3-ethereum', 
    query_paths=query_paths,
    filter_dict = {'tokenIn_symbol': 'WETH', 'amountOutUSD_lt': .001}
    )

print(df.head(5))