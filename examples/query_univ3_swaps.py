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

token_in = ['0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48'] # USDC
token_out = ['0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2'] # WETH

# specify query size
query_size = 500

df = my_dex.query_swap_data(
    start_time=start_time, 
    end_time=end_time, 
    query_size=query_size,
    token_in = token_in,
    token_out = token_out,
    save_data=True,
    saved_file_name='usdc_weth_query',
    add_endpoint_col=True
    )