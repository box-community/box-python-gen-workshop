from typing import Dict, List, Optional

from box_sdk_gen import (
    AiAgentAsk,
    AiResponseFull,
    Authentication,
    BaseObject,
    CreateAiAskItems,
    FetchOptions,
    FetchResponse,
    NetworkSession,
    fetch,
    prepare_params,
    serialize,
    to_string,
)
from box_sdk_gen.serialization import deserialize

from utils.ai_schemas import IntelligenceMetadataSuggestions, IntelligenceResponse


class ExtractStructuredMetadataTemplate(BaseObject):
    def __init__(
        self,
        scope: Optional[str] = None,
        template_key: Optional[str] = None,
        type: Optional[str] = "metadata_template",
    ):
        """
        param scope: The scope of the metadata template can either be global or at the enterprise level. The global scope is used for templates that are available to any Box enterprise. The enterprise_ scope represents templates that have been created within a specific enterprise, where * will be the ID of that enterprise.
        type scope: str
        param template_key: The name of the metadata template.
        type template_key: str
        param type: always "metadata_template".
        """
        self.scope = scope
        self.template_key = template_key
        self.type = type


class ExtractStructuredFieldOption(BaseObject):
    def __init__(self, key: str):
        self.key = key

    def __repr__(self):
        return f"Option(key='{self.key}')"


class ExtractStructuredField(BaseObject):
    def __init__(
        self,
        key: Optional[str] = None,
        type: Optional[str] = None,
        description: Optional[str] = None,
        display_name: Optional[str] = None,
        prompt: Optional[str] = None,
        options: Optional[List[ExtractStructuredFieldOption]] = None,
        **kwargs,
    ):
        """
        param key: A unique identifier for the field.
        type key: str
        param type: The type of the field. Can include but is not limited to string, float, date, enum, and multiSelect.
        type type: str
        param description: A description of the field.
        type description: str
        param display_name: The display name of the field.
        type display_name: str
        param prompt: Context about the key that may include how to find and how to format it.
        type prompt: str
        param options: A list of options for this field. This is most often used in combination with the enum and multiSelect field types.
        type options: List[ExtractStructuredFieldOption]
        """
        super().__init__(**kwargs)
        self.key = key
        self.type = type
        self.description = description
        self.display_name = display_name
        self.prompt = prompt
        self.options = options


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

    # region deprecated code
    # def intelligence_ask(
    #     self,
    #     mode: IntelligenceMode,
    #     prompt: str,
    #     items: List[IntelligenceItem],
    #     extra_headers: Optional[Dict[str, Optional[str]]] = None,
    # ) -> IntelligenceResponse:
    #     """
    #     Sends an intelligence request to supported LLMs and returns an answer.
    #     :param mode: The mode specifies if this request is qa or hubs_qa
    #     depending on what client it is supporting.
    #     :type mode: CreateIntelligenceSendIntelligenceRequestModeArg
    #     :param prompt: The prompt provided by the client to be answered
    #     by the LLM.
    #     :type prompt: str
    #     :param items: The items to be processed by the LLM, often files.
    #     :type items: List[CreateIntelligenceSendIntelligenceRequestItemsArg]
    #     :param extra_headers: Extra headers that will be included
    #     in the HTTP request.
    #     :type extra_headers: Optional[Dict[str, Optional[str]]], optional
    #     """
    #     if extra_headers is None:
    #         extra_headers = {}
    #     request_body: Dict = {"mode": mode, "prompt": prompt, "items": items}
    #     headers_map: Dict[str, str] = prepare_params({**extra_headers})
    #     response: FetchResponse = fetch(
    #         "".join([self.network_session.base_urls.base_url, "/ai/ask"]),
    #         FetchOptions(
    #             method="POST",
    #             headers=headers_map,
    #             data=serialize(request_body),
    #             content_type="application/json",
    #             response_format="json",
    #             auth=self.auth,
    #             network_session=self.network_session,
    #         ),
    #     )
    #     return deserialize(response.data, IntelligenceResponse)

    # def intelligence_text_gen(
    #     self,
    #     prompt: str,
    #     items: List[IntelligenceItem],
    #     dialogue_history: Optional[List[IntelligenceItem]] = None,
    #     extra_headers: Optional[Dict[str, Optional[str]]] = None,
    # ) -> IntelligenceResponse:
    #     """
    #     Sends an intelligence request to supported LLMs and returns an answer.
    #     :param prompt: The prompt provided by the client to be answered
    #     by the LLM.
    #     :type prompt: str
    #     :param items: The items to be processed by the LLM, often files.
    #     :type items: List[
    #         CreateIntelligenceSendIntelligenceTextGenRequestItemsArg
    #         ]
    #     :param dialogue_history: The context given along with a prompt
    #     to inform a response from the LLM.
    #     :type dialogue_history:
    #     Optional[List[
    #         CreateIntelligenceSendIntelligenceTextGenRequestDialogueHistoryArg
    #         ]], optional
    #     :param extra_headers: Extra headers that will be included
    #     in the HTTP request.
    #     :type extra_headers: Optional[Dict[str, Optional[str]]], optional
    #     """
    #     if extra_headers is None:
    #         extra_headers = {}
    #     request_body: Dict = {
    #         "prompt": prompt,
    #         "items": items,
    #         "dialogue_history": dialogue_history,
    #     }
    #     headers_map: Dict[str, str] = prepare_params({**extra_headers})
    #     response: FetchResponse = fetch(
    #         "".join([self.network_session.base_urls.base_url, "/ai/text_gen"]),
    #         FetchOptions(
    #             method="POST",
    #             headers=headers_map,
    #             data=serialize(request_body),
    #             content_type="application/json",
    #             response_format="json",
    #             auth=self.auth,
    #             network_session=self.network_session,
    #         ),
    #     )
    #     return deserialize(response.data, IntelligenceResponse)

    # endregion

    # region Intelligence custom code
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

    def extract(
        self,
        # mode: CreateAiAskMode,
        prompt: str,
        items: List[CreateAiAskItems],
        *,
        # dialogue_history: Optional[List[AiDialogueHistory]] = None,
        include_citations: Optional[bool] = None,
        ai_agent: Optional[AiAgentAsk] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None,
    ) -> AiResponseFull:
        if extra_headers is None:
            extra_headers = {}
        request_body: Dict = {
            # 'mode': mode,
            "prompt": prompt,
            "items": items,
            # 'dialogue_history': dialogue_history,
            "include_citations": include_citations,
            "ai_agent": ai_agent,
        }
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = fetch(
            FetchOptions(
                url="".join([self.network_session.base_urls.base_url, "/2.0/ai/extract"]),
                method="POST",
                headers=headers_map,
                data=serialize(request_body),
                content_type="application/json",
                response_format="json",
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, AiResponseFull)

    def extract_structured(
        self,
        items: List[CreateAiAskItems],
        fields: List[ExtractStructuredField],
        metadata_template: Optional[ExtractStructuredMetadataTemplate] = None,
        *,
        include_citations: Optional[bool] = None,
        ai_agent: Optional[AiAgentAsk] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None,
    ) -> AiResponseFull:
        if extra_headers is None:
            extra_headers = {}
        request_body: Dict = {
            "items": items,
            "fields": fields,
            "metadata_template": metadata_template,
            "include_citations": include_citations,
            "ai_agent": ai_agent,
        }
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = fetch(
            FetchOptions(
                url="".join([self.network_session.base_urls.base_url, "/2.0/ai/extract_structured"]),
                method="POST",
                headers=headers_map,
                data=serialize(request_body),
                content_type="application/json",
                response_format="json",
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        ai_answer = AiResponseFull(answer=response.data, created_at=response.headers.get("date"))
        return ai_answer
        # return deserialize(response.data, AiResponseFull)


# endregion
