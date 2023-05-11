from queryportal.subgraphinterface import SubgraphInterface

import polars as pl
pl.Config.set_fmt_str_lengths(200)

# load hosted endpoint
sgi = SubgraphInterface(endpoints=[
    'https://api.thegraph.com/subgraphs/name/messari/uniswap-v3-ethereum'
                     ])

# load decentralized endpoint
sgi.subject.load_decentralized_endpoints({'univ3_decentralized': 'https://api.playgrounds.network/v1/proxy/subgraphs/id/G3JZhmKKHC4mydRzD6kSz5fCWve5WDYYCyTFSJyv3SD5'})

# print subgraph keys
print(f'subgraph endpoints: {sgi.subject.subgraphs.keys()}')

my_dict = sgi.subject.getQueryPaths(sgi.subject.subgraphs['univ3_decentralized'], 'swaps')

# print fields for swaps entity
print(f'my dict fields for univ3_decentralized swaps entity: {my_dict.keys()}')

query_paths = list(my_dict.keys())
query_size = 2500

df1 = sgi.query_entity(
    query_size=query_size,
    entity='swaps',
    name='uniswap-v3-ethereum',
    query_paths=query_paths 
    )
print(df1.head(5))

df2 = sgi.query_entity(
    query_size=query_size,
    entity='swaps',
    name='univ3_decentralized',
    query_paths=query_paths 
    )

print(df2.head(5))