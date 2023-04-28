from functools import  cache
from typing import Any, Dict


from subgrounds import Subgrounds
from subgrounds.schema import TypeRef
from subgrounds.subgraph import SyntheticField
from subgrounds.subgraph.fieldpath import FieldPath



##############################################
# FieldPath Helpers
##############################################
@cache
def get_subgrounds():
    """
    Returns a `Subgrounds` object representing a collection of subgrounds. The `@cache` decorator
    ensures that the `Subgrounds` object returned by this function is cached and returned on subsequent
    calls to this function, rather than being recomputed every time. 

    """
    return Subgrounds()

def match_query_paths(default_query_path: FieldPath, query_paths: list[str] = None) -> FieldPath | list[FieldPath]:
    """
    Matches query_paths to query_path_cols
    """
    match query_paths:
        case None:
            return default_query_path
        case _:
            return create_query_path(default_query_path, query_paths)
        
def create_query_path(default_query_path: FieldPath, query_paths: list[str]) -> list[FieldPath]:
    """
    Generates a list of fieldpaths from a list of strings
    """
    new_query_path_list = []
    for variable in query_paths:
        # TODO - add a check statement. Do not split if variable doesn't belong to an entity...
        variable_parts = variable.split('_')    # split if need to split
        modified_qp = default_query_path  # start with new qp
        # #DEBUG print statement
        # print(f'DEBUG - query path: {default_query_path}')
        # # get column names for default_query_path
        # col_list = list((field.name, TypeRef.graphql(field.type_)) for field in default_query_path)
        # print(f'col list: {col_list}')



        for i in range(len(variable_parts)):
            modified_qp = modified_qp._select(variable_parts[i])
        new_query_path_list.append(modified_qp)
    return new_query_path_list


def create_filter_dict(filter_dict: dict) -> dict:
    """
    Takes the query filter dictionary input and reformats it with nested dictionaries, if required, to conform to Subgrounds query input.
    """

    if len(filter_dict) != 0:   # check if filter_dict is empty. If it is not, continue.
        keyword_list = ['in', 'not', 'gt', 'gte', 'lt', 'lte', 'not_in', 'contains', 'not_contains']

        output_dict = {}

        for key in filter_dict.keys():
            # check if last _ is followed by keyword. Split into a list
            key_parts = key.split('_')
            if key_parts[-1] in keyword_list:   # check if key ends with a keyword
                # combine key_parts[-1] and key_parts[-2]
                new_key = '_'.join(key_parts[-2:])
                # drop the last two elements from key_parts
                key_parts = key_parts[:-2]
                # append new_key
                key_parts.append(new_key)

        # make a new dictionary based off of the key_parts
        temp_dict = output_dict
        for i in range(len(key_parts)):
            if key_parts[i] not in temp_dict:
                if i == len(key_parts) - 1:
                    temp_dict[key_parts[i]] = {}
                    temp_dict[key_parts[i]] = filter_dict[key]
                else:
                    new_key = key_parts[i] + '_'
                    temp_dict[new_key] = {}
                    temp_dict = temp_dict[new_key]

        return output_dict

    else:               # if filter_dict is empty, return an empty dictionary. Note we need to return an empty dictionary instead of a None value because Subgrounds requires a dictionary as a required input
        print('filter_dict is empty. Returning empty dictionary')
        return {}
    








def synthetic_convert(type, deps) -> SyntheticField:
    """
    NOTE - Currently not being used
    Creates a new synthetic field path with a different type
    """
    match type:
        case SyntheticField.STRING:
            return SyntheticField(lambda value: str(value), SyntheticField.STRING, deps)
        case SyntheticField.INT:
            return SyntheticField(lambda value: int(value), SyntheticField.INT, deps)
        case SyntheticField.FLOAT:
            return SyntheticField(lambda value: float(value), SyntheticField.FLOAT, deps)
        case SyntheticField.BOOL:
            return SyntheticField(lambda value: bool(value), SyntheticField.BOOL, deps)