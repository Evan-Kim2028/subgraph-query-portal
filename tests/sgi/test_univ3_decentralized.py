from queryportal.subgraphinterface import SubgraphInterface

import polars as pl
pl.Config.set_fmt_str_lengths(200)

# instantiate Dex class with subgraph key
# ETH = G3JZhmKKHC4mydRzD6kSz5fCWve5WDYYCyTFSJyv3SD5
# ARB = FQ6JYszEKApsBpAmiHesRsd9Ygc6mzmpNRANeVQFYoVX
sgi = SubgraphInterface(endpoints={'univ3_decentralized': 'https://api.playgrounds.network/v1/proxy/subgraphs/id/G3JZhmKKHC4mydRzD6kSz5fCWve5WDYYCyTFSJyv3SD5'})

print(f'subject endpoints: {sgi.subject.subgraphs.keys()}')


df2 = sgi.query_entity(
    entity='deposits',
    name='univ3_decentralized'
    )

print(df2.head(5))