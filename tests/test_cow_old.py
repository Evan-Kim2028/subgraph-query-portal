from queryportal.cow import Cow
from datetime import datetime, timedelta


# Cow Subgraph endpoint
endpoint = 'https://api.thegraph.com/subgraphs/name/cowprotocol/cow'

# instantiate Cow class. Cow stores Cow-related query functions
my_cow = Cow(endpoint)

# define a filter dictionary to customize the query search
filter_dict = {
    'timestamp_gte': int((datetime.today() - timedelta(days=1)).timestamp()),
    'timestamp_lte': int(datetime.today().timestamp())
}

# specify query size
query_size = 2500

df = my_cow.query_trades(
    query_size=query_size,
    filter_dict=filter_dict,    
    token_names=True,           # currently unused
    save_data=True,
    add_endpoint_col=True
    )


# group dataframe by trades_settlement_id
# assuming 'df' is the DataFrame you want to group
grouped_df = df.groupby('trades_settlement_id').count()

# sorted by settlement_id count size
grouped_df.sort_values(by='trades_settlement_id', ascending=False)