from queryportal.dex import Dex
from datetime import datetime


# define subgraph endpoint. This one is the Univ3 Ethereum endpoint maintained by Messari
endpoint = 'https://api.thegraph.com/subgraphs/name/messari/uniswap-v3-ethereum'

# instantiate dex class. Dex stores dex-related query functions
my_dex = Dex(endpoint)

# define start and end dates for query range. 
start_date = datetime(2023, 3, 9)
end_date = datetime(2023, 3, 13)

# convert dates from datetime to unix timestamp
start_time = my_dex.date_to_time(start_date)
end_time = my_dex.date_to_time(end_date)

# specify query size
query_size = 2500


df = my_dex.query_swaps(
    start_time=start_time, 
    end_time=end_time, 
    query_size=query_size,
    save_data=True,
    saved_file_name='univ3_all_swaps',
    add_endpoint_col=True
    )