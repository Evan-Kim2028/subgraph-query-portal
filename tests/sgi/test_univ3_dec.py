from queryportal.subgraphinterface import SubgraphInterface

import polars as pl
pl.Config.set_fmt_str_lengths(200)

# instantiate Dex class with subgraph key
eth = 'G3JZhmKKHC4mydRzD6kSz5fCWve5WDYYCyTFSJyv3SD5'
arb = 'FQ6JYszEKApsBpAmiHesRsd9Ygc6mzmpNRANeVQFYoVX'
sgi = SubgraphInterface(endpoints={'univ3_decentralized': f'https://api.playgrounds.network/v1/proxy/subgraphs/id/{eth}'})

print(f'subject endpoints: {sgi.subject.subgraphs.keys()}')

# print(f'schema for univ3_decentralized: {sgi.subject.subgraphs["univ3_decentralized"]._schema}')

df2 = sgi.query_entity(
    entity='swaps',
    name='univ3_decentralized'
    )

print(df2.head(5))