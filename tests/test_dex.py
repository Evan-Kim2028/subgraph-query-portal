from queryportal.dex import Dex
from datetime import datetime


# define subgraph endpoint. This one is the Univ3 Ethereum endpoint maintained by Messari
endpoint = 'https://api.thegraph.com/subgraphs/name/messari/uniswap-v3-ethereum'

# instantiate dex class. Dex stores dex-related query functions
my_dex = Dex(endpoint)

# define a filter dictionary to customize the query search
filter_dict = {
    'timestamp_gte': int(datetime(2023, 3, 9).timestamp()),
    'timestamp_lte': int(datetime(2023, 3, 13).timestamp())
}

# specify query size
query_size = 2500

df = my_dex.query_swaps(
    query_size=query_size,
    # filter_dict=filter_dict,
    token_names=True,
    save_data=True,
    add_endpoint_col=True
    )
