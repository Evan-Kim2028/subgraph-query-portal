from queryportal.cow import Cow
from datetime import datetime


# Cow Subgraph endpoint
endpoint = 'https://api.thegraph.com/subgraphs/name/cowprotocol/cow'

# instantiate Cow class. Cow stores Cow-related query functions
my_cow = Cow(endpoint)

# define a filter dictionary to customize the query search
filter_dict = {
    'timestamp_gte': int(datetime(2023, 3, 9).timestamp()),
    'timestamp_lte': int(datetime(2023, 3, 13).timestamp())
}

# specify query size
query_size = 2500

df = my_cow.query_trades(
    query_size=query_size,
    filter_dict=filter_dict,
    token_names=True,
    save_data=True,
    add_endpoint_col=True
    )