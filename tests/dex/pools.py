from queryportal.dex import Dex

# define subgraph endpoint. This one is the Univ3 Ethereum endpoint maintained by Messari
endpoint = 'https://api.thegraph.com/subgraphs/name/messari/uniswap-v3-arbitrum'
# endpoint = 'https://api.thegraph.com/subgraphs/name/messari/balancer-v2-ethereum'

# instantiate dex class. Dex stores dex-related query functions
my_dex = Dex(endpoint)

df = my_dex.query_liquiditypools(
    add_endpoint_col=True)


print('done')