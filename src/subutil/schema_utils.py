
from typing import Any, Dict, Type


from subgrounds import Subgrounds
from subgrounds.subgraph import Subgraph
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


def getColFields(sg: Subgrounds, schema_str: str):
    """
    getColFields gets a list of fields from the swaps_entity schema.
    """
    return list((field.name, TypeRef.graphql(field.type_)) for field in sg.__getattribute__(schema_str)._object.fields)



## These classes are used to generate dictionary objects from schema fields. Not sure if they are useful or not at this time (4.25.23)
class DynamicClassGenerator:
    @staticmethod
    def create(name: str, class_vars: Dict[str, Any]) -> Type:
        return type(name, (), class_vars)


class MyFixedClass(DynamicClassGenerator):
    def __init__(self, **kwargs):
        super().__init__()
        for k, v in kwargs.items():
            setattr(self, k, v)