from usdc_depeg.dex import Dex
from datetime import datetime


# define variables
endpoint = 'https://api.thegraph.com/subgraphs/name/messari/balancer-v2-arbitrum'


# instantiate class
my_dex = Dex(endpoint)

# define start and end dates for query range
start_date = datetime(2023, 3, 9)
end_date = datetime(2023, 3, 13)

# variables needed for query_swap_data()
start_time = my_dex.datetime_to_timestamp(start_date)
end_time = my_dex.datetime_to_timestamp(end_date)
query_size = 10000000

df = my_dex.query_swap_data(
    start_time=start_time, 
    end_time=end_time, 
    query_size=query_size
    )

# get values of endpoint after the last /
file_name = endpoint.split('/')[-1]

# save polars dataframe to parquet 
df.write_parquet(f'data/{file_name}_swaps.parquet')

print('done')