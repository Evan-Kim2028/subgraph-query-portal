from subutil.subject import Subject

sub = Subject('https://api.thegraph.com/subgraphs/name/messari/uniswap-v3-ethereum')


print(list(sub.subgraphs.keys())[0])

sg_key = list(sub.subgraphs.keys())[0]

sg_obj = sub.subgraphs[sg_key]


my_list = sub.getSubgraphSchema(sg_obj)
print(my_list)


# my_list = sub.get_entity_cols(my_list[0])

print('done')