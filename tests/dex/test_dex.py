from queryportal.dex import Dex
from datetime import datetime, timedelta

# define subgraph endpoint. This one is the Univ3 Ethereum endpoint maintained by Messari
endpoint = 'https://api.thegraph.com/subgraphs/name/messari/uniswap-v3-arbitrum'

# instantiate dex class. Dex stores dex-related query functions
my_dex = Dex(endpoint)



my_dex.query_firehose(query_size=250)


#####################################################
# Test functionality of individual queries
#
#####################################################
# my_dex.query_swaps()
# my_dex.query_pools()
# my_dex.query_tokens()


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