from subutil.subject import Subject

endpoint = 'https://api.thegraph.com/subgraphs/name/messari/uniswap-v3-ethereum'
# load Subject
sub = Subject(endpoint)


print(f'subject endpoints: {sub.endpoints}')

# test load schema logic
query_dict = sub.load_schema(sub.subgraphs['uniswap-v3-ethereum'])
# print(type(query_dict)) # dict
print(f'keys are {query_dict.keys()}')

print(f' one of the keys are swaps and it is type {type(query_dict["swaps"])}')