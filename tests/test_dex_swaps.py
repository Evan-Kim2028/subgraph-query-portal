from queryportal.dex import Dex
from datetime import datetime


# define subgraph endpoint. This one is the Univ3 Ethereum endpoint maintained by Messari
endpoint = 'https://api.thegraph.com/subgraphs/name/messari/uniswap-v3-ethereum'

# instantiate dex class. Dex stores dex-related query functions
my_dex = Dex(endpoint)

# define start and end dates for query range. 
start_time = datetime(2023, 3, 9)
end_time = datetime(2023, 3, 13)

# convert start_time and end_time to unix timestamps
start_timestamp = int(start_time.timestamp())
end_timestamp = int(end_time.timestamp())

# define a filter dictionary to customize the query search
filter_dict = {
    'timestamp_gte': start_timestamp,
    'timestamp_lte': end_timestamp
}

# specify query size
query_size = 2500

df = my_dex.query_swaps(
    query_size=query_size,
    # filter_dict=filter_dict,
    save_data=True,
    add_endpoint_col=True
    )
