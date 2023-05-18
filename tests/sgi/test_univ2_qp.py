from queryportal.subgraphinterface import SubgraphInterface

import polars as pl
pl.Config.set_fmt_str_lengths(200)

# HOSTED
# sgi = SubgraphInterface(endpoints=['https://api.thegraph.com/subgraphs/name/messari/uniswap-v3-ethereum'])

# Decentralized
sgi = SubgraphInterface(endpoints={
    # https://thegraph.com/explorer/subgraphs/ELUcwgpm14LKPLrBRuVvPvNKHQ9HvwmtKgKSH6123cr7?view=Overview&chain=mainnet
    'uniswa-v2-ethereum': 'https://api.playgrounds.network/v1/proxy/subgraphs/id/2szAn45skWZFLPUbxFEtjiEzT1FMW8Ff5ReUPbZbQxtt'
    })


# print subgraph keys
univ3_dict = sgi.subject.getQueryPaths(sgi.subject.subgraphs['uniswa-v2-ethereum'], 'swaps')


# print fields for swaps entity
print(f'my dict fields for univ3_decentralized swaps entity: {list(univ3_dict.keys())}')

query_size = 1500

query_paths = ['timestamp', 'id', 'amount0In', 'amount1In', 'pair_id']

univ2 = sgi.query_entity(
    query_size=query_size,
    entity='swaps',
    query_paths = query_paths,
    orderBy='amount1In',
    filter_dict={'amount1In_gt': 1000},
    name='uniswa-v2-ethereum', 
    )

print(univ2)
