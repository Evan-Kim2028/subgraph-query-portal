from subutil.subject import Subject

endpoint = 'https://api.thegraph.com/subgraphs/name/messari/uniswap-v3-ethereum'    # hosted endpoint
    # decentralized endpoint


# load Subject with hosted service endpoints
sub = Subject(endpoint)
print(f'subject endpoints: {sub.subgraphs.keys()}')

# load decentralized endpoint
sub.load_decentralized_endpoints(
    {'univ3_decentralized': 'https://api.playgrounds.network/v1/proxy/subgraphs/id/G3JZhmKKHC4mydRzD6kSz5fCWve5WDYYCyTFSJyv3SD5'    # decentralized endpoint
     }
     )

print(f'subject endpoints: {sub.subgraphs.keys()}')



# test load schema logic
query_dict = sub.load_schema(sub.subgraphs['univ3_decentralized'])
print(query_dict.keys())

# print(type(query_dict)) # dict
print(f' one of the keys are swaps and it is type {type(query_dict["swaps"])}')