from queryportal.subgraphinterface import SubgraphInterface as sgi

import polars as pl
pl.Config.set_fmt_str_lengths(200)

endpoints = [
    'https://api.thegraph.com/subgraphs/name/messari/uniswap-v3-ethereum',
    'https://api.thegraph.com/subgraphs/name/messari/uniswap-v3-arbitrum',
    'https://api.thegraph.com/subgraphs/name/messari/uniswap-v3-polygon',
    'https://api.thegraph.com/subgraphs/name/messari/uniswap-v3-optimism',
]

# instantiate univ3 class with subgraph key
univ3 = sgi(endpoints=endpoints)

query_paths = [
    'hash',
    'pool_name', 
    'tokenIn_symbol', 
    'tokenOut_symbol', 
    'amountOutUSD', 
    'amountInUSD',
    'amountOut',
    'amountIn',
    ]

filter_dict = {'tokenIn_symbol': "WETH"}

for subgraph_name in list(univ3.subject.subgraphs.keys()):
    print('subgraph_name: ', subgraph_name)
    df = univ3.query_entity(
        entity='swaps',
        name=subgraph_name,
        query_paths=query_paths,
        filter_dict=filter_dict,
        )
    print(df.head(5))