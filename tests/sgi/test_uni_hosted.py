from queryportal.subgraphinterface import SubgraphInterface

import polars as pl
pl.Config.set_fmt_str_lengths(200)

# instantiate Dex class with subgraph key
sgi = SubgraphInterface(endpoints=[
    'https://api.thegraph.com/subgraphs/name/messari/uniswap-v3-ethereum'
                     ])

sgi.subject.load_decentralized_endpoints({'univ3_decentralized': 'https://api.playgrounds.network/v1/proxy/subgraphs/id/G3JZhmKKHC4mydRzD6kSz5fCWve5WDYYCyTFSJyv3SD5'})

print(f'subject endpoints: {sgi.subject.subgraphs.keys()}')


df1 = sgi.query_entity(
    entity='swaps',
    name='uniswap-v3-ethereum', 
    )
print(df1.head(5))


df2 = sgi.query_entity(
    entity='swaps',
    name='univ3_decentralized',
    )

print(df2.head(5))