from queryportal.dex import Dex
from datetime import datetime


# define subgraph endpoint. This one is the Univ3 Ethereum endpoint maintained by Messari
endpoint = 'https://api.thegraph.com/subgraphs/name/messari/uniswap-v3-arbitrum'
# endpoint = 'https://api.thegraph.com/subgraphs/name/messari/balancer-v2-ethereum'

# instantiate dex class. Dex stores dex-related query functions
my_dex = Dex(endpoint)

# # convert start_time and end_time to unix timestamps
# start_timestamp = int(datetime(2023, 3, 9).timestamp())
# end_timestamp = int(datetime(2023, 3, 13).timestamp())

# # define a filter dictionary to customize the query search
# filter_dict = {
#     'timestamp_gte': start_timestamp,
#     'timestamp_lte': end_timestamp,
# }

# specify query size
query_size = 125

df = my_dex.query_swaps(
    query_size=query_size,
    # filter_dict=filter_dict,
    save_data=True,
    add_endpoint_col=True
    )
