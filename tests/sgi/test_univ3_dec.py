from queryportal.subgraphinterface import SubgraphInterface

import polars as pl
pl.Config.set_fmt_str_lengths(200)

# instantiate Dex class with subgraph key
eth = 'G3JZhmKKHC4mydRzD6kSz5fCWve5WDYYCyTFSJyv3SD5' # indexed on ethereum
arb = 'FQ6JYszEKApsBpAmiHesRsd9Ygc6mzmpNRANeVQFYoVX' # indexed on arbitrum



sgi = SubgraphInterface(
    endpoints={'univ3_eth': f'https://api.playgrounds.network/v1/proxy/subgraphs/id/{eth}',
                # 'univ3_arb': f'https://api.playgrounds.network/v1/proxy/subgraphs/id/{arb}'
               }
    )

print(f'subject endpoints: {sgi.subject.subgraphs.keys()}')




df1 = sgi.query_entity(
    entity='deposits',
    name='univ3_arb'
    )

print(df1.head(5))

df2 = sgi.query_entity(
    entity='deposits',
    name='univ3_eth'
    )

print(df2.head(5))