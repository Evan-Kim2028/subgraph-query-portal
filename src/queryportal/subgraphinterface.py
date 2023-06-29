import polars as pl

from dataclasses import dataclass

from queryportal.polars_utils import *
from subutil.subject import Subject
from subutil.fieldpath_utils import *

@dataclass
class SubgraphInterface:
    """
    `SubgraphInterface` is an interface wrapper that can be used over any Subgraph and provides a 
    standardized way to interact with Subgraphs. 
    """
    endpoints: str | list[str]
    subject: Subject = None

    def __post_init__(self):
        self.subject = Subject(self.endpoints)

    def query(
            self, 
            query_path: FieldPath | list[FieldPath],
            saved_file_name: str = None,
            graphql_query_fmt: bool = False
            ) -> pl.DataFrame:
        """
        `query` is an internal method used by `query_entity` that sends `query_path`, which is a list of `FieldPath` Subgrounds objects to Subgrounds and returns a polars DataFrame of the query results.
        """

        if graphql_query_fmt:
            graphql_query_path = self.subject.sg.mk_request(query_path).graphql
            print(f'graphql query path: {graphql_query_path}')

        # Obtain json dict of query results
        query_dict = self.subject.sg.query_json(query_path)

        # get nested json key. Subgrounds creates a hash blob for internal purposes so we need the keys that come after the hash blob.
        first_key = next(iter(query_dict[0].keys()))

        # check if the first key is empty. If it is then return an error message
        if query_dict[0][first_key] == []:
            print(f'query_dict[0][first_key] is empty: {query_dict[0][first_key]}')
            return
        
        pl_df = pl.from_dicts(query_dict[0][first_key])

        # convert structs to columns
        pl_df = fmt_dict_cols(pl_df)
        # convert lists to columns
        final_df = fmt_arr_cols(pl_df)

        # If a file name is provided, save the dataframe as a parquet file
        if saved_file_name is not None:
            save_file(final_df, saved_file_name)

        # Return the converted dataframe
        return final_df
    

    @timeit
    @df_describe
    def query_entity(self, name: str = None, entity:str = None, query_size=5, query_paths: list[str] = None, orderBy: str = None,  block_filter = {}, filter_dict={}, saved_file_name=None, graphql_query_fmt=False) -> pl.DataFrame:
        """
        `query_entity` is the main query method for querying Subgraphs. 
        
        Parameters
        ----------
        name : str
            name of the subgraph

        entity : str
            name of the subgraph entity being queried

        query_size : int
            number of results to return. Default is 5.

        query_paths : list[str]
            list of fieldpaths that will be queried. If not provided, the method will query all fields by default.

        orderBy : str
            fieldpath to order the query results by. If not provided, the method will not order the results.

        block_filter : dict
            `block` is a special keyword that access archival indexer states based on the block number. Default is an empty dictionary which is equivalent to not using the filter.

        filter_dict : dict
            query filter parameters stored as a dictionary

        saved_file_name : str
            name of the file to save the query results as. If not provided, the query results will not be saved.
    
        Returns
        -------
        pl.DataFrame
            Polars DataFrame of queried rows
        """

        # First, process the name for single/multi endpoint inputs.
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

        # create modified filter dict that conforms to required Subgrounds query format
        new_filter_dict = create_filter_dict(filter_dict)

        match orderBy:
            case None:
                # no order is specified
                generic_qp = query_dict[entity](
                    first = query_size,
                    where = new_filter_dict,
                    block = block_filter
                )
            case _:
                # order is specified
                generic_qp = query_dict[entity](
                    first = query_size,
                    where = new_filter_dict,
                    orderBy = orderBy,
                    orderDirection = "desc",
                    block = block_filter
                )
        
        matched_query_path = match_query_paths(query_paths=query_paths, default_query_path = generic_qp)
        
        return self.query(
                    query_path=matched_query_path,
                    saved_file_name=saved_file_name,
                    graphql_query_fmt=graphql_query_fmt
                )
