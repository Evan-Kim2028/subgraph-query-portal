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
token_out = ['0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48'] # USDC
# leave out token_in on purpose to make sure filters work as optional params

# specify query size
query_size = 123


df = my_dex.query_swap_data(
    start_time=start_time, 
    end_time=end_time, 
    query_size=query_size,
    token_out = token_out,
    save_data=True,
    add_endpoint_col=True
    )

print('finished')