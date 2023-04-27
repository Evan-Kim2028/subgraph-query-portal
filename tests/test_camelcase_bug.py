from queryportal.subgraphinterface import SubgraphInterface as sgi

import polars as pl
pl.Config.set_fmt_str_lengths(200)

endpoints = ['https://api.thegraph.com/subgraphs/name/denverbaumgartner/rubiconv2-optimism-mainnet',
             'https://api.thegraph.com/subgraphs/name/denverbaumgartner/rubiconv2-optimism-goerli',
             'https://api.thegraph.com/subgraphs/name/denverbaumgartner/rubiconv2-arbitrum-goerli',
             'https://api.thegraph.com/subgraphs/name/denverbaumgartner/rubiconv2-polygon-mumbai'
             ]


sgi = sgi(endpoints=endpoints)

query_paths = [     # THERES A BUG, CAN'T PARSE THE COLUMNS BECAUSE OF THE COLUMN NAME FORMAT!!
    # 'id',
    'transaction_timestamp',
    # 'transaction_block_number',
    # 'transaction_block_index',
    # 'index',
    # 'maker_id',
    # 'pay_gem',
    'buy_gem',
    # 'pay_amt',
    # 'buy_amt',
    # 'paid_amt',
    # 'bought_amt',
    # 'open',
    # 'removed_timestamp',
    # 'removed_block'
]


df1 = sgi.query_entity(
    entity='offers',
    name='rubiconv2-optimism-mainnet',
    query_paths=query_paths
)

print(df1)