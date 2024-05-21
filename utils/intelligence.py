from typing import Optional


from typing import List

from typing import Dict

from box_sdk_gen import to_string

from box_sdk_gen.serialization import serialize

from box_sdk_gen.serialization import deserialize

from utils.ai_schemas import (
    IntelligenceResponse,
    IntelligenceMode,
    IntelligenceItem,
    IntelligenceMetadataSuggestions,
)

from box_sdk_gen import Authentication

from box_sdk_gen import NetworkSession

from box_sdk_gen import prepare_params

from box_sdk_gen import fetch

from box_sdk_gen import FetchOptions

from box_sdk_gen import FetchResponse


class IntelligenceManager:
    def __init__(
        self,
        auth: Optional[Authentication] = None,
        network_session: Optional[NetworkSession] = None,
    ):
        if network_session is None:
            network_session = NetworkSession()
        self.auth = auth
        self.network_session = network_session

    def intelligence_ask(
        self,
        mode: IntelligenceMode,
        prompt: str,
        items: List[IntelligenceItem],
        extra_headers: Optional[Dict[str, Optional[str]]] = None,
    ) -> IntelligenceResponse:
        """
        Sends an intelligence request to supported LLMs and returns an answer.
        :param mode: The mode specifies if this request is qa or hubs_qa
        depending on what client it is supporting.
        :type mode: CreateIntelligenceSendIntelligenceRequestModeArg
        :param prompt: The prompt provided by the client to be answered
        by the LLM.
        :type prompt: str
        :param items: The items to be processed by the LLM, often files.
        :type items: List[CreateIntelligenceSendIntelligenceRequestItemsArg]
        :param extra_headers: Extra headers that will be included
        in the HTTP request.
        :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        request_body: Dict = {"mode": mode, "prompt": prompt, "items": items}
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = fetch(
            "".join([self.network_session.base_urls.base_url, "/ai/ask"]),
            FetchOptions(
                method="POST",
                headers=headers_map,
                data=serialize(request_body),
                content_type="application/json",
                response_format="json",
                auth=self.auth,
                network_session=self.network_session,
            ),
        )
        return deserialize(response.data, IntelligenceResponse)

    def intelligence_text_gen(
        self,
        prompt: str,
        items: List[IntelligenceItem],
        dialogue_history: Optional[List[IntelligenceItem]] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None,
    ) -> IntelligenceResponse:
        """
        Sends an intelligence request to supported LLMs and returns an answer.
        :param prompt: The prompt provided by the client to be answered
        by the LLM.
        :type prompt: str
        :param items: The items to be processed by the LLM, often files.
        :type items: List[
            CreateIntelligenceSendIntelligenceTextGenRequestItemsArg
            ]
        :param dialogue_history: The context given along with a prompt
        to inform a response from the LLM.
        :type dialogue_history:
        Optional[List[
            CreateIntelligenceSendIntelligenceTextGenRequestDialogueHistoryArg
            ]], optional
        :param extra_headers: Extra headers that will be included
        in the HTTP request.
        :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        request_body: Dict = {
            "prompt": prompt,
            "items": items,
            "dialogue_history": dialogue_history,
        }
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = fetch(
            "".join([self.network_session.base_urls.base_url, "/ai/text_gen"]),
            FetchOptions(
                method="POST",
                headers=headers_map,
                data=serialize(request_body),
                content_type="application/json",
                response_format="json",
                auth=self.auth,
                network_session=self.network_session,
            ),
        )
        return deserialize(response.data, IntelligenceResponse)

    def intelligence_metadata_suggestion(
        self,
        item: str,
        scope: str,
        template_key: str,
        confidence: str = "experimental",
        extra_headers: Optional[Dict[str, Optional[str]]] = None,
    ) -> IntelligenceResponse:
        if extra_headers is None:
            extra_headers = {}
        query_params_map: Dict[str, str] = prepare_params(
            {
                "item": to_string("file_" + item),
                # "item": to_string("file_" + item),
                "scope": to_string(scope),
                "template_key": to_string(template_key),
                "confidence": to_string(confidence),
            }
        )
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = fetch(
            "".join(
                [
                    self.network_session.base_urls.base_url,
                    "/2.0/metadata_instances/suggestions",
                ]
            ),
            FetchOptions(
                method="GET",
                params=query_params_map,
                headers=headers_map,
                response_format="json",
                auth=self.auth,
                network_session=self.network_session,
            ),
        )
        return deserialize(response.data, IntelligenceMetadataSuggestions)
