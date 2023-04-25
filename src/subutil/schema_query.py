
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

def getQueryFields(sg: Subgrounds, schema: str) -> list[str]:
    """
    Get all queryable fields from the subgraph schema.
    :return: list[str] of queryable fields from the subgraph schema
    """
    query_field_paths = getSchemaFields(sg, schema)

    # fields that do not end with s are not queryable.
    return [field for field in query_field_paths if field.endswith('s')]

def getSchemaFields(sg: Subgrounds, schema_str: str) -> list[str]:
    """
    getSubgraphField gets a fields list from a subgraph schema.
    :param str schema_str: Schema object name to get fields list from
    :param str operation: Enter one of the following - 'Query', 'Mutation', or 'Subscription'. Default is 'Query' because that is most commonly used.
    :return: strings field list from a Subgraph schema
    """
    return list(field.name for field in sg.__getattribute__(schema_str)._object.fields)

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