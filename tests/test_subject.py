from subutil.subject import Subject
from queryportal.new_dex import Dex


dex_endpoints = [
    'https://api.thegraph.com/subgraphs/name/messari/uniswap-v3-ethereum',
    'https://api.thegraph.com/subgraphs/name/messari/uniswap-v3-arbitrum',
    'https://api.thegraph.com/subgraphs/name/messari/uniswap-v3-polygon',
    'https://api.thegraph.com/subgraphs/name/messari/uniswap-v3-optimism',
]

# loading the Subject with dex_endpoints
subject = Subject(dex_endpoints)

# instantiate Dex class with subgraph key
dex = Dex(subject=subject)

print(f'Loaded dex_endpoints: {list(dex.subject.subgraphs.keys())}')

filter_dict = {
    'tokenIn_symbol': 'WETH'
}

query_paths = [
    'hash',
    'pool_name', 
    # 'pool_inputTokens_name', #This is a nested struct. Although there is logic to handle a single struct, it is not yet implemented for nested structs. Not sure if it should be either.
    'tokenIn_symbol', 
    'tokenOut_symbol', 
    'amountOutUSD', 
    'amountInUSD',
    'amountOut',
    'amountIn',
    ]

for subgraph_name in list(dex.subject.subgraphs.keys()):
    df = dex.query_swaps(
    subgraph_name=subgraph_name, 
    query_paths=query_paths,
    filter_dict = filter_dict
    )

    print(df.head(5))













print('done')