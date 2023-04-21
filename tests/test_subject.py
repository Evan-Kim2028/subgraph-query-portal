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


# run a query like normal with 'uniswap-v3-ethereum' key
univ3_eth = dex.query_swaps(subgraph_name='uniswap-v3-ethereum')
univ3_arb = dex.query_swaps(subgraph_name='uniswap-v3-arbitrum')

















print('done')