from typing import Optional

from box_sdk_gen.client import BoxClient, NetworkSession
from box_sdk_gen import Authentication
from utils.intelligence import IntelligenceManager


class BoxAIClient(BoxClient):
    """Box AI Client"""

    def __init__(
        self,
        auth: Authentication,
        network_session: Optional[NetworkSession] = None,
    ):
        """Initialize the Box AI Client"""
        super().__init__(auth=auth, network_session=network_session)
        self.intelligence = IntelligenceManager(auth=auth, network_session=network_session)
