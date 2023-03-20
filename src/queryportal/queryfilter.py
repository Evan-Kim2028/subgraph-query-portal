from dataclasses import dataclass

@dataclass
class QueryFilter():
    """
    Functionality Layout:
    make_search_param constructs a customized search filter that is inserted
    into the where clause in the query_df function in the Subgrounds class.
    """


    def make_search_param(
            self,             
            start_time: int = None, 
            end_time: int = None, 
            token_in: list[str] = None,
            token_out: list[str] = None,
            ) -> dict:
        """
        make_search_param constructs a search parameter query. This is used upstream to get passed into the
        query_swap function. The filter parameters are specified based off of the search_param dictionary keys.
        """
        
        # empty query dict that will be filled up and returned.
        search_query_dict = {}

        # check variable type. For any None type, do not add to query dictionary
        if self.check_type(start_time) is not None:
            search_query_dict['timestamp_gte'] = start_time
        if self.check_type(end_time) is not None:
            search_query_dict['timestamp_lt'] = end_time
        if self.check_type(token_in) is not None:
            search_query_dict['tokenIn_in'] = token_in
        if self.check_type(token_out) is not None:
            search_query_dict['tokenOut_in'] = token_out

        return search_query_dict
        
    def check_type(self, variable):
        """
        Helper function checks the variable type. If the variable type 
        """
        match variable:
            case int():
                print(f'{variable} is {type(variable)}')
                return variable
            case list():
                for element in variable:
                    if not isinstance(element, str):
                        print(f'Type Mismatch: {element} is {type(element)} and needs to contain all strings. However it contains {element}, which is type {type(element)}, which is not a string. Return None')
                        return None
                return variable            
            case Other:
                print(f'Type Mismatch: {variable} is {type(variable)}. Return None')
                return None
            