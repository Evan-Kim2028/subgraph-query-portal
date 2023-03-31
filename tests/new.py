from queryportal.dex import Dex
from datetime import datetime, timedelta
import polars as pl



arbitrum = [
    'https://api.thegraph.com/subgraphs/name/messari/balancer-v2-arbitrum',
    'https://api.thegraph.com/subgraphs/name/messari/curve-finance-arbitrum',
    'https://api.thegraph.com/subgraphs/name/messari/sushiswap-arbitrum',
    # 'https://api.thegraph.com/subgraphs/name/messari/uniswap-v3-arbitrum'     # doesn't work, Overflow Error: Python int too long to convert to C long
]

dex_data = []
for endpoint in arbitrum:
    print(f'endpoint: {endpoint}')
    # instantiate dex class. Dex stores dex-related query functions
    my_dex = Dex(endpoint)

    # convert start_time and end_time to unix timestamps
    start_timestamp = int(datetime(2023, 3, 9).timestamp())
    end_timestamp = int(datetime(2023, 3, 13).timestamp())

    # define a filter dictionary to customize the query search
    filter_dict = {
        'timestamp_gte': int((datetime.today() - timedelta(days=1)).timestamp()),
        'timestamp_lte': int(datetime.today().timestamp())
    }

    # specify query size
    query_size = 5

    df = my_dex.query_swaps(
        query_size=query_size,
        # filter_dict=filter_dict,
        save_data=True,
        add_endpoint_col=True
        )
    
    dex_data.append(df)


# concat dex_data list of polars dataframes
dex_df = pl.concat(dex_data)

dex_df.head(5)
