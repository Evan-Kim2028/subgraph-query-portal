from subutil.subject import Subject
from subutil.schema_utils import *

from collections import OrderedDict

#####################################################################
# This file is for testing the schema_query.py module functionality.
# CURRENTLY A WORK IN PROGRESS!
#####################################################################


# 1) Load Subject with endpoints.
sub = Subject([
    'https://api.thegraph.com/subgraphs/name/messari/uniswap-v3-ethereum',
    'https://api.thegraph.com/subgraphs/name/messari/uniswap-v3-arbitrum'
    ])


# 2a) Retrieve Subgraph endpoint key.
sg_key = list(sub.subgraphs.keys())[0]

# 2b) Load subgraph object
sg_obj = sub.subgraphs[sg_key]

# 2c) Get all schema entities
schema_list = getSubgraphSchema(sg_obj)
print(schema_list)

# 2d) Get Schema Fields
schema_fields = getSchemaFields(sg_obj, schema_list[0])
# print(f'\n{schema_list[0]} schema_fields: {schema_fields.keys()}')
print(schema_fields["positions"])
print(f'type is {type(schema_fields["positions"])}')    # fieldmeta type

# 3) Select queryable schema entities
query_field = getQueryFields(sg_obj, schema_list[schema_list.index('Query')])
print(f'\nAll queryable fields are: {query_field}\n')
print(f'type is {type(query_field)}\n')    # dict type
print(f'\n{query_field["positions"]}')



# get col fields
col_fields = getColFields(sg_obj, schema_list[0])
print(f'\n{schema_list[0]} col_fields: {col_fields}')   # the value outputs are just strings...

# TEST STUFF
col_dict = OrderedDict(col_fields)
print(f'\ndict: {col_dict}')

concrete_obj = DynamicClassGenerator.create('MyDynamicClass', col_dict)
print(concrete_obj.deposits)


# concrete_obj = MyFixedClass(**col_dict)
# print(concrete_obj.account)


print('\ndone')