from queryportal.queryfilter import QueryFilter
from datetime import datetime



test_qf = QueryFilter()

start_time = 100
end_time = 110
token_in = ['WETH']
token_out = ['USDC']

# create search query dict with type checking.
param_dict = test_qf.make_search_param(start_time, end_time, token_in, token_out)
