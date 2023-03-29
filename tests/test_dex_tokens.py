from queryportal.dex import Dex
from queryportal.helpers import *



# define subgraph endpoint. This one is the Univ3 Ethereum endpoint maintained by Messari
endpoint = 'https://api.thegraph.com/subgraphs/name/messari/uniswap-v3-ethereum'

# instantiate dex class. Dex stores dex-related query functions
my_dex = Dex(endpoint)

# specify query size
query_size = 2500

swap_df = my_dex.query_swaps(
    query_size=query_size,
    save_data=True,
    add_endpoint_col=True
    )


token_in_list = swap_df['swaps_tokenIn_id'].unique().to_list()
print(len(token_in_list))

token_df = my_dex.query_tokens(
    query_size=query_size,
    filter_dict={'id_in': token_in_list},
    save_data=True,
    add_endpoint_col=True
    )


# create a dictionary of token ids and their symbols
token_dict = dict(zip(token_df['tokens_id'], token_df['tokens_symbol']))

merge_output = synthetic_merge(token_dict)

