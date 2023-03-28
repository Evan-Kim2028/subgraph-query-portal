from queryportal.dex import Dex
from datetime import datetime


# define subgraph endpoint. This one is the Univ3 Ethereum endpoint maintained by Messari
endpoint_list = [
                'https://api.thegraph.com/subgraphs/name/messari/uniswap-v3-ethereum',
                'https://api.thegraph.com/subgraphs/name/messari/uniswap-v3-polygon',
                'https://api.thegraph.com/subgraphs/name/messari/uniswap-v3-arbitrum',
                'https://api.thegraph.com/subgraphs/name/messari/uniswap-v3-optimism'
                 ]

for endpoint in endpoint_list:
    # instantiate dex class. Dex stores dex-related query functions
    my_dex = Dex(endpoint)

    # define start and end dates for query range. 
    start_time = datetime(2023, 3, 9)
    end_time = datetime(2023, 3, 13)

    token_in = ['USD Coin']

    # specify query size
    query_size = 2500


    df = my_dex.query_swaps(
        start_time=start_time, 
        end_time=end_time, 
        query_size=query_size,
        token_in=token_in,
        save_data=True,
        saved_file_name='usdc_into_univ3',
        add_endpoint_col=True
        )