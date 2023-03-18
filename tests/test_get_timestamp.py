from usdc_depeg.dex import Dex
from datetime import datetime


endpoint = 'https://api.thegraph.com/subgraphs/name/messari/uniswap-v3-ethereum'


my_dex = Dex()

start_date = datetime(2023, 3, 9)
end_date = datetime(2023, 3, 12)

start_timestamp = my_dex.date_to_time(start_date)
end_timestamp = my_dex.date_to_time(end_date)

print(f'start_timestamp: {start_timestamp}')
print(f'end_timestamp: {end_timestamp}')

