from dataclasses import dataclass, field
from subutil.helpers import *

from subgrounds import Subgrounds
from subgrounds.schema import TypeRef
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


    def getSubgraphSchema(self) -> list[str]:
        """
        getSubgraphSchema gets the Subgraph schema and returns a list.
        """
        return list(name for name, type_ in self.subgraph._schema.type_map.items() if type_.is_object)


    