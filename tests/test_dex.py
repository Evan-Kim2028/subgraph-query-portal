from dex import Dex
from datetime import datetime


# define variables
endpoint = 'https://api.thegraph.com/subgraphs/name/messari/uniswap-v3-ethereum'


# instantiate class
my_dex = Dex(endpoint)

# define start and end dates for query range
start_date = datetime(2023, 3, 9)
end_date = datetime(2023, 3, 13)

# variables needed for query_swap_data()
start_time = my_dex.date_to_time(start_date)
end_time = my_dex.date_to_time(end_date)
query_size = 123

df = my_dex.query_swap_data(
    start_time=start_time, 
    end_time=end_time, 
    query_size=query_size,
    save_data=False,
    add_endpoint_col=True
    )