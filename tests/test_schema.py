from subutil.subject import Subject
from subutil.helpers import *

sub = Subject([
    'https://api.thegraph.com/subgraphs/name/messari/uniswap-v3-ethereum',
    'https://api.thegraph.com/subgraphs/name/messari/uniswap-v3-arbitrum'
    ])


# get first subgraph endpoint key
sg_key = list(sub.subgraphs.keys())[0]

# load subgraph object for the specific endpoint key
sg_obj = sub.subgraphs[sg_key]

# get all schema entities
schema_list = getSubgraphSchema(sg_obj)
print(f'\nschema_list: \n{schema_list}')

# select queryable schema entities
schema_fp_list = schema_list.index('Query')

query_field = getQueryFields(sg_obj, schema_list[schema_fp_list])
print(f'\nquery_field: \n{query_field}')

print(f'\nthe first query field is: {query_field[0]}')
# schema_list = sub.get_entity_cols(schema_list[0])


print('\ndone')