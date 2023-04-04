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
my_dex.query_firehose(query_paths = ['pool_name', 'tokenIn_name', 'tokenOut_name'])


#####################################################
# Test functionality of individual queries
#
#####################################################
# my_dex.query_swaps(query_paths = ['id', 'timestamp'])
# my_dex.query_pools()
# my_dex.query_tokens(query_paths = ['id', 'symbol'])


#####################################################
# Test functionality of query with filter dict
#
#####################################################
# filter_dict = {
#     'timestamp_gte': int((datetime.today() - timedelta(days=1)).timestamp()),
#     'timestamp_lte': int(datetime.today().timestamp())
# }
# my_dex.query_swaps(filter_dict = filter_dict)



print('done')