from queryportal.dex import Dex
from datetime import datetime


# define subgraph endpoint. This one is the Univ3 Ethereum endpoint maintained by Messari
endpoint = 'https://api.thegraph.com/subgraphs/name/messari/uniswap-v3-ethereum'

# instantiate dex class. Dex stores dex-related query functions
my_dex = Dex(endpoint)

# specify query size
query_size = 2500

df = my_dex.query_swaps(
    query_size=query_size,
    save_data=True,
    saved_file_name='query_univ3_latest',
    add_endpoint_col=True
    )