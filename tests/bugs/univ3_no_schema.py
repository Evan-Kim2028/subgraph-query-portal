from queryportal.subgraphinterface import SubgraphInterface
from datetime import datetime, timedelta

import polars as pl
pl.Config.set_fmt_str_lengths(200)

# HOSTED
# sgi = SubgraphInterface(endpoints=['https://api.thegraph.com/subgraphs/name/messari/uniswap-v3-ethereum'])

# Decentralized
sgi = SubgraphInterface(endpoints={
    # https://thegraph.com/explorer/subgraphs/ELUcwgpm14LKPLrBRuVvPvNKHQ9HvwmtKgKSH6123cr7?view=Overview&chain=mainnet
    'uniswap-v3-ethereum': 'https://api.playgrounds.network/v1/proxy/subgraphs/id/ELUcwgpm14LKPLrBRuVvPvNKHQ9HvwmtKgKSH6123cr7'
    })


# print subgraph keys
univ3_dict = sgi.subject.getQueryPaths(sgi.subject.subgraphs['uniswap-v3-ethereum'], 'swaps')


# print fields for swaps entity
print(f'my dict fields for univ3_decentralized swaps entity: {list(univ3_dict.keys())}')

# there appears to be something corrupted in these fieldpaths...
# query_paths = ['hash', 'to', 'from', 'blockNumber', 'timestamp', 'tokenIn', 'amountIn', 'amountInUSD', 'tokenOut', 'amountOut', 'amountOutUSD', 'pool']

query_paths = [
    'hash',
    'to',
    'from',
    'blockNumber',
    'timestamp',
    'tokenIn_symbol',
    'tokenOut_symbol',
    'amountIn',
    'amountOut',
    'pool_id'
]

filter = {
    'timestamp_gte': int((datetime(2023, 5, 17).timestamp())),
    'timestamp_lte': int(datetime(2023, 5, 18).timestamp()),
    # 'amountInUSD_gte': 10,
    # 'amountOutUSD_gte': 10
    # 'hash': "0xb2d071e74709bddc8ab005aa42ce4251ad77453fed195f856b46d055c88cb556"
}

query_size = 1000

univ3 = sgi.query_entity(
    query_size=query_size,
    entity='swaps',
    name='uniswap-v3-ethereum', 
    # query_paths=query_paths,
    filter_dict = filter,
    orderBy='timestamp',
    block_filter = {'number_gte': 17315261},
    # saved_file_name='univ3_swaps'
    graphql_query_fmt=True
    )


print(univ3.shape[0])