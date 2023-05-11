from subutil.subject import Subject
from subutil.schema_utils import *
from subutil.word_utils import *

from collections import OrderedDict

#####################################################################
# This file is for testing the schema_query.py module functionality.
# CURRENTLY A WORK IN PROGRESS!
#####################################################################


# 1) Load Subject with endpoints.
# sub = Subject([
#     'https://api.thegraph.com/subgraphs/name/messari/uniswap-v3-ethereum',
#     'https://api.thegraph.com/subgraphs/name/messari/uniswap-v3-arbitrum'
#     ])

# instantiate Dex class with subgraph key
eth = 'G3JZhmKKHC4mydRzD6kSz5fCWve5WDYYCyTFSJyv3SD5'
arb = 'FQ6JYszEKApsBpAmiHesRsd9Ygc6mzmpNRANeVQFYoVX'
sub = Subject({'univ3_decentralized': f'https://api.playgrounds.network/v1/proxy/subgraphs/id/{eth}'})



# 2a) Retrieve Subgraph endpoint key.
sg_key = list(sub.subgraphs.keys())[0]

# 2b) Load subgraph object
sg = sub.subgraphs[sg_key]

# 2c) Get all schema entities
schema_entity_list = getSubgraphSchema(sg)
print(schema_entity_list)

# 2d) Get Schema Fields
# schema_fields = getSchemaFields(sg, schema_entity_list[0])
# print(f'\nschema_fields for "swaps": {schema_fields["swaps"]}')
# print(schema_fields["swaps"])
# print(f'swaps type is {type(schema_fields["swaps"])}')    # fieldmeta type

# 3) Select queryable schema entities
query_field = getQueryFields(sg, schema_entity_list[schema_entity_list.index('Query')])
print(f'\nAll queryable fields are: {query_field.keys()}\n')

query_entity_list = list(query_field.keys())

levenshtein_dict = make_levenshtein_dict(query_entity_list, schema_entity_list)

print(f'\nLevenshtein dict: {levenshtein_dict}')


# get cols using Levenshtein dict
col_fields = getColFields(sg, levenshtein_dict['swaps'])
col_fields_dict = {key: value for key, value in col_fields}

print(col_fields_dict.keys())
print('\ndone')















# # TEST STUFF
# col_dict = OrderedDict(col_fields)
# print(f'\ndict: {col_dict}')


# concrete_obj = DynamicClassGenerator.create('MyDynamicClass', col_dict)
# print(concrete_obj)


# concrete_obj = MyFixedClass(**col_dict)
# print(concrete_obj.account)

