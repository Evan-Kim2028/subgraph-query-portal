from subutil.subject import Subject
from queryportal.new_dex import Dex


dex_endpoints = [
    'https://api.thegraph.com/subgraphs/name/messari/uniswap-v3-ethereum',
    'https://api.thegraph.com/subgraphs/name/messari/uniswap-v3-arbitrum'
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
    # 'timestamp', 
    # 'hash',
    'pool_name', 
    # 'pool_inputTokens_name', # this returns an array of values which doubles amount of rows due to flattening logic in Subgrounds
    'tokenIn_symbol', 
    'tokenOut_symbol', 
    # 'amountOutUSD', 
    # 'amountInUSD',
    # 'amountOut',
    # 'amountIn',
    ]


# run a query like normal with 'uniswap-v3-ethereum' key
univ3_eth = dex.query_swaps(
    subgraph_name='uniswap-v3-ethereum', 
    query_paths=query_paths,
    filter_dict = filter_dict
    )
univ3_arb = dex.query_swaps(
    subgraph_name='uniswap-v3-arbitrum',
    query_paths=query_paths,
    filter_dict = filter_dict
    )


print(univ3_eth.head(5))
print(univ3_arb.head(5))














print('done')