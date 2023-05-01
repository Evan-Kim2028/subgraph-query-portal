from queryportal.subgraphinterface import SubgraphInterface

import polars as pl
pl.Config.set_fmt_str_lengths(200)

# instantiate Dex class with subgraph key
sgi = SubgraphInterface(endpoints={'univ3_decentralized': 'https://api.playgrounds.network/v1/proxy/subgraphs/id/FQ6JYszEKApsBpAmiHesRsd9Ygc6mzmpNRANeVQFYoVX'})

print(f'subject endpoints: {sgi.subject.subgraphs.keys()}')


df2 = sgi.query_entity(
    entity='tokens',
    name='univ3_decentralized'
    )

print(df2.head(5))