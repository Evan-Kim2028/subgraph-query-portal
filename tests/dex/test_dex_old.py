from queryportal.dex import Dex
from datetime import datetime, timedelta

# define subgraph endpoint. This one is the Univ3 Ethereum endpoint maintained by Messari
endpoint = 'https://api.thegraph.com/subgraphs/name/messari/uniswap-v3-arbitrum'

# fieldpaths for added typing protection with pylance,pyright


# instantiate dex class. Dex stores dex-related query functions
my_dex = Dex(endpoint)


#####################################################
# Test firehose (complex query)
#
#####################################################
my_dex.query_firehose()
# my_dex.query_firehose(query_paths = 'pool_id')


#####################################################
# Test functionality of individual queries
#
#####################################################
# my_dex.query_swaps()
# my_dex.query_pools()
# my_dex.query_tokens(query_paths = ['id', 'symbol'])


#####################################################
# Test functionality of query with filter dict
#
#####################################################
# filter_dict = {
#     'timestamp_gte': int((datetime.today() - timedelta(days=1)).timestamp()),
#     'timestamp_lte': int(datetime.today().timestamp()),
#     'token_symbol_in': ['USDC', 'WETH'],
#     'pool_id_in': ['0x8ad599c3a0ff1de082011efddc58f1908eb6e6d8']
# }
# my_dex.query_swaps(filter_dict = filter_dict)



print('done')