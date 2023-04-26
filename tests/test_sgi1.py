from queryportal.subgraphinterface import SubgraphInterface as sgi

import polars as pl
pl.Config.set_fmt_str_lengths(200)

# instantiate Dex class with subgraph key
sgi = sgi(endpoints=[
    'https://api.thegraph.com/subgraphs/name/messari/uniswap-v3-ethereum', 
    'https://api.thegraph.com/subgraphs/name/cowprotocol/cow'
                     ])

df1 = sgi.query_entity(
    entity='swaps',
    name='uniswap-v3-ethereum', 
    )
print(df1.head(5))


df2 = sgi.query_entity(
    entity='trades',
    name='cow'
    )

print(df2.head(5))

# index in a polars dataframe vs pandas dataframe?
# need a 'standard' index to pivot onto. Need the same minutes to be contained on the data