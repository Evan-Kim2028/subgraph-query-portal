from dotenv import load_dotenv
import os

from dataclasses import dataclass, field
from subutil.fieldpath_utils import *
from subutil.schema_utils import *
from subutil.word_utils import *

from subgrounds import Subgrounds
from subgrounds.subgraph import Subgraph

########################################################
# Subject is a collection of Subgrounds objects. 
# Manage a collection of Subgraphs via subgraph endpoint keys.
########################################################

@dataclass
class Subject:
    """
    Mnages the Subgrounds object for queryportal classes.
    Collection of subgraph endpoints.
    """
    initial_endpoints: str | list[str] | dict  # instantiate class with this variable

    subgraphs: dict[str, Subgraph] = field(default_factory=dict)    # empty dict that gets populated on init
    sg: Subgrounds = field(default_factory=get_subgrounds)      # default subgrounds configuration

    def __post_init__(self):
        # load dex subgraph schema information from the the subgraph initial_endpoints. This is represented as a Subgraph object.
        self.load_endpoints(self.initial_endpoints)

    def load_endpoints(self, endpoints: str | list[str]):
        """
        loads subgraph endpoints into Subgrounds. This is used to initialize endpoints into Subject
        at the time of instantiation. For the moment, you can only initialize with hosted endpoints.
        Use load_decentralized_endpoints() to add decentralized endpoints
        """
        if isinstance(endpoints, list):
            for endpoint in endpoints:
                self.subgraphs[endpoint.split('/')[-1]] = self.sg.load(endpoint)
        if isinstance(endpoints, str):
                self.subgraphs[endpoints.split('/')[-1]] = self.sg.load(endpoints)
        if isinstance(endpoints, dict):
            self._update_header()
            for key, value in endpoints.items():
                self.subgraphs[key] = self.sg.load(value)

    def _update_header(self):
         """
         _update_header() is used to update the header of the Subgrounds object. If the header is None, it will be updated
         to the playgrounds api key in the .env file.
         """
         if self.sg.headers["Playgrounds-Api-Key"] is None:
            # check if .env file exists with try/except
            try:
                load_dotenv()
                self.sg.headers["Playgrounds-Api-Key"] = os.environ['PG_KEY']
            except ValueError:
                print('No .env file found. Please add a .env file with your playgrounds api key.')


    def load_decentralized_endpoints(self, endpoints: dict):
        """
        loads decentralized subgraph endpoints into the Subgrounds object. Call this after loading hosted service endpoints.
        Endpoints is a dict as opposed to a string or list so that the names of the endpoints can be customized.
        """

        # add playgrounds api key to header.
        self._update_header()

        # for each endpoint in the endpoints dict, load the endpoint into the Subgrounds object and update the subgraphs dict
        for key, value in endpoints.items():
            self.subgraphs[key] = self.sg.load(value)


    def load_schema(self, sg: Subgraph) -> dict:
        """
        loads subgraph schema into Subgrounds
        """
        # 2c) Get all schema entities
        schema_list = getSubgraphSchema(sg)

        # 3) Select queryable schema entities
        query_field_dict = getQueryFields(sg, schema_list[schema_list.index('Query')])
        
        return_dict = {}
        # for every value in query_field_dict keys, get the field path and add it to the return dict
        for key in query_field_dict.keys():
            return_dict[key] = getFieldPath(sg, key)
            
        # print(f' Queryable schema entities: {return_dict.keys()}')
        
        return return_dict

    def getQueryPaths(self, sg: Subgrounds, entity_str: str) -> dict:
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

    



    