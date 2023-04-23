from dataclasses import dataclass, field
from subutil.helpers import *

from subgrounds import Subgrounds
from subgrounds.schema import TypeRef, SchemaMeta
from subgrounds.subgraph import Subgraph
from subgrounds.subgraph import SyntheticField


@dataclass
class Subject:
    """
    Mnages the Subgrounds object for queryportal classes.
    Collection of subgraph endpoints.
    """
    endpoints: str | list[str]  # instantiate class with this variable

    subgraphs: dict[str, Subgraph] = field(default_factory=dict)    # empty dict that gets populated on init
    sg: Subgrounds = field(default_factory=get_subgrounds)      # default subgrounds configuration

    def __post_init__(self):
        # load dex subgraph schema information from the the subgraph endpoints. This is represented as a Subgraph object.
        self.load_endpoints(self.endpoints)

    def load_endpoints(self, endpoints: str | list[str]):
        """
        loads subgraph endpoints into Subgrounds
        """
        if isinstance(endpoints, list):
            for endpoint in endpoints:
                self.subgraphs[endpoint.split('/')[-1]] = self.sg.load(endpoint)
        if isinstance(endpoints, str):
                self.subgraphs[endpoints.split('/')[-1]] = self.sg.load(endpoints)


    def getQueryFields(self, endpoint: str, schema: str) -> list[str]:
        """
        Get all queryable fields from the subgraph schema.
        :return: list[str] of queryable fields from the subgraph schema
        """
        query_field_paths = self.getSchemaFields(endpoint, schema)

        return query_field_paths


    def getSchemaFields(self, endpoint: str, schema_str: str) -> list[str]:
        """
        getSubgraphField gets a fields list from a subgraph schema.
        :param str schema_str: Schema object name to get fields list from
        :param str operation: Enter one of the following - 'Query', 'Mutation', or 'Subscription'. Default is 'Query' because that is most commonly used.
        :return: strings field list from a Subgraph schema
        """
        return list(field.name for field in self.subgraphs[endpoint].__getattribute__(schema_str)._object.fields)
    

    def getSubgraphSchema(self, sg: Subgraph) -> list[str]:
        """
        getSubgraphSchema gets the Subgraph schema and returns a list.
        """
        return list(name for name, type_ in sg._schema.type_map.items() if type_.is_object)
    



    