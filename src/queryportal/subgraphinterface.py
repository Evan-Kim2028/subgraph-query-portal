import polars as pl

from dataclasses import dataclass

from queryportal.polars_utils import *
from subutil.subject import Subject
from subutil.fieldpath_utils import *

@dataclass
class SubgraphInterface:
    """
    SubgraphInterface class stores standardized Messari SubgraphInterface query methods for easier access. 
    The queries assume that Messari schemas and may not function properly if used with non-Messari standardized Dex subgraphs.
    """
    endpoints: str | list[str]
    subject: Subject = None

    def __post_init__(self):
        self.subject = Subject(self.endpoints)

    def query(
            self, 
            query_path: FieldPath | list[FieldPath],
            saved_file_name: str = None,
            add_endpoint_col: bool = True
            ) -> pl.DataFrame:
        """
        new query method that uses query_json() instead of query_df(). Placeholder comment.
        """
        # Obtain json dict of query results
        df = self.subject.sg.query_json(query_path)

        # get nested json key. Subgrounds creates a hash blob for internal purposes so we need the keys that come after the hash blob.
        first_key = next(iter(df[0].keys()))

        pl_df = pl.from_dicts(df[0][first_key])

        # convert structs to columns
        pl_df = fmt_dict_cols(pl_df)
        # convert lists to columns
        final_df = fmt_arr_cols(pl_df)

        # If a file name is provided, save the dataframe as a CSV file
        if saved_file_name is not None:
            save_file(final_df, saved_file_name)

        # drop json "id". Seems to return by default even if it's not queried. Seems to be part of json blob structure
        final_df = final_df.drop('id')
        # Return the converted dataframe
        return final_df
    

    @timeit
    @df_describe
    def query_entity(self, entity:str = None, name: str = None, query_paths: list[str] = None, query_size=5, filter_dict={}, saved_file_name=None, add_endpoint_col=True) -> pl.DataFrame:
        """
        This method constructs a query from an entity. It takes in query parameters as inputs and returns a 
        Polars DataFrame of the query results. The method also adds a datetime column to the swaps entity by converting the 
        timestamp column to datetime format using a synthetic field. The `add_endpoint_col` parameter is used to add the 
        endpoint column to the query results if set to True.
        """

        # first we process the name for single/multi value inputs.
        if name == None:
            try:
                assert len(self.subject.subgraphs) == 1 # check that there is only 1 subgraph endpoint loaded
                single_key = list(self.subject.subgraphs.keys())
                sg_key = self.subject.subgraphs[single_key[0]]
                print(f'Querying endpoint: {single_key[0]}')
            except AssertionError:
                print(f'{len(self.subject.subgraphs)} endpoints were loaded. Please specify 1 subgraph name.')
                return
        else:
            # load subgraph from the key name
            sg_key = self.subject.subgraphs[name]
            print(f'Querying endpoint: {name}')

        # get schema
        query_dict = self.subject.load_schema(sg_key)

        print(f' Queryable entities: {query_dict.keys()}')

        # create modified filter dict that conforms to required Subgrounds query format
        new_filter_dict = create_filter_dict(filter_dict)

        # define query search params based off of filter_dict
        generic_qp = query_dict[entity](
            first=query_size,
            where = new_filter_dict
        )

        matched_query_path = match_query_paths(query_paths=query_paths, default_query_path = generic_qp)
        
        return self.query(
                    query_path=matched_query_path,
                    saved_file_name=saved_file_name,
                    add_endpoint_col=add_endpoint_col
                )
