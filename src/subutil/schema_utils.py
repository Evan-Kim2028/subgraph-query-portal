
from typing import Any, Dict, Type

from subutil.word_utils import *

from subgrounds import Subgrounds
from subgrounds.subgraph import Subgraph, FieldPath
from subgrounds.schema import TypeRef


##################################################################
# Collection of functions that help query schema information from a Subgraph
##################################################################

def getSubgraphSchema(sg: Subgraph) -> list[str]:
    """
    getSubgraphSchema gets the Subgraph schema and returns a list.
    """
    return list(name for name, type_ in sg._schema.type_map.items() if type_.is_object)

# def getSchemaFields(sg: Subgrounds, schema_str: str) -> dict:
#     """
#     getSubgraphField gets a fields list from a subgraph schema.
#     :param str schema_str: Schema object name to get fields list from
#     :param str operation: Enter one of the following - 'Query', 'Mutation', or 'Subscription'. Default is 'Query' because that is most commonly used.
#     :return: strings field list from a Subgraph schema
#     """
    
#     return list(field.name for field in sg.__getattribute__(schema_str)._object.fields)

def getSchemaFields(sg: Subgrounds, schema_str: str) -> dict:
    """
    getSubgraphField gets a fields list from a subgraph schema.
    :param str schema_str: Schema object name to get fields list from
    :param str operation: Enter one of the following - 'Query', 'Mutation', or 'Subscription'. Default is 'Query' because that is most commonly used.
    :return: dictionary containing field names and their types from a Subgraph schema
    """
    fields_dict = {}
    fields = sg.__getattribute__(schema_str)._object.fields # its a list type
    for field in fields:
        fields_dict[field.name] = field
    return fields_dict


def getQueryFields(sg: Subgrounds, schema: str) -> dict:
    """
    Get all queryable fields from the subgraph schema by filtering out fields that end with s
    """
    query_schema_dict = getSchemaFields(sg, schema)

    # if query_schema_dict key ends with s, then remove from dictionary
    for key in list(query_schema_dict.keys()):
        if not key.endswith('s'):
            # print(f'removed {key}')
            del query_schema_dict[key]

    return query_schema_dict

def getFieldPath(sg: Subgrounds, field: str,  operation: str ='Query') -> FieldPath:
    """
    DEPRECATED, currently not used: 
    
    getFieldPath converts a string to a FieldPath object. In a Subgrounds query, the format follows subgrounds.schema.FieldPath.
    :param str field: Enter the string that will be converted to a FieldPath
    :param str operation: Enter one of the following - 'Query', 'Mutation', or 'Subscription'. Default is 'Query' because that is most commonly used. 
    :return: FieldPath object
    """
    return sg.__getattribute__(operation).__getattribute__(field)
    

def getColFields(sg: Subgrounds, schema_str: str):
    """
    getColFields gets a list of fields from the schema.
    """
    return list((field.name, TypeRef.graphql(field.type_)) for field in sg.__getattribute__(schema_str)._object.fields)

def getQueryPaths(sg: Subgrounds, entity_str: str) -> dict:
    """
    Returns all fields from the queryable entity
    """

    # Get Subgraph Schema Entities
    schema_entity_list = getSubgraphSchema(sg)
    # Get Queryable Subgraph Entities
    query_field = getQueryFields(sg, schema_entity_list[schema_entity_list.index('Query')])

    # turn query fields from dict to list
    query_entity_list = list(query_field.keys())

    # compute lvenshtein distance dict
    levenshtein_dict = make_levenshtein_dict(query_entity_list, schema_entity_list)

    # get cols using Levenshtein dict
    col_fields = getColFields(sg, levenshtein_dict[entity_str])
    col_fields_dict = {key: value for key, value in col_fields}

    return col_fields_dict