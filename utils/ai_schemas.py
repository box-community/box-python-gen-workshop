from enum import Enum

from typing import Optional

from box_sdk_gen.base_object import BaseObject

from typing import List, Dict


class IntelligenceMode(str, Enum):
    MULTIPLE_ITEM_QA = "multiple_item_qa"
    SINGLE_ITEM_QA = "single_item_qa"


class IntelligenceItemType(str, Enum):
    FILE = "file"


class IntelligenceItem(BaseObject):
    def __init__(
        self,
        id: Optional[str] = None,
        type: Optional[IntelligenceItemType] = None,
        content: Optional[str] = None,
        **kwargs,
    ):
        """
        :param id: The id of the item
        :type id: Optional[str], optional
        :param type: The type of the item
        :type type: Optional[IntelligenceItemsFieldTypeField], optional
        :param content: The content of the item, often the text representation.
        :type content: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type
        self.content = content


class Intelligence(BaseObject):
    def __init__(
        self,
        mode: IntelligenceMode,
        prompt: str,
        items: List[IntelligenceItem],
        **kwargs,
    ):
        """
        :param mode: The mode specifies if this request is qa or hubs_qa
                     depending on what client it is supporting.
        :type mode: IntelligenceModeField
        :param prompt: The prompt provided by the client to be answered
                       by the LLM.
        :type prompt: str
        :param items: The items to be processed by the LLM, often files.
        :type items: List[IntelligenceItemsField]
        """
        super().__init__(**kwargs)
        self.mode = mode
        self.prompt = prompt
        self.items = items


class IntelligenceDialogueHistory(BaseObject):
    def __init__(
        self,
        prompt: Optional[str] = None,
        answer: Optional[str] = None,
        created_at: Optional[str] = None,
        **kwargs,
    ):
        """
        :param prompt: The prompt provided by the client to be answered
                       by the LLM.
        :type prompt: Optional[str], optional
        :param answer: The answer provided by the LLM.
        :type answer: Optional[str], optional
        :param created_at: The ISO date formatted timestamp of when the
                           answer to the prompt was created.
        :type created_at: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.prompt = prompt
        self.answer = answer
        self.created_at = created_at


class IntelligenceTextGen(BaseObject):
    def __init__(
        self,
        prompt: str,
        items: List[IntelligenceItem],
        dialogue_history: Optional[List[IntelligenceDialogueHistory]] = None,
        **kwargs,
    ):
        """
        :param prompt: The prompt provided by the client to be answered
                        by the LLM.
        :type prompt: str
        :param items: The items to be processed by the LLM, often files.
        :type items: List[IntelligenceTextGenItemsField]
        :param dialogue_history: The context given along with a prompt
                                    to inform a response from the LLM.
        :type dialogue_history: Optional[
                                            List[
                                                IntelligenceTextGenDialogueHistoryField
                                                ]
                                        ], optional
        """
        super().__init__(**kwargs)
        self.prompt = prompt
        self.items = items
        self.dialogue_history = dialogue_history


class IntelligenceResponse(BaseObject):
    def __init__(
        self,
        answer: str,
        created_at: str,
        completion_reason: Optional[str] = None,
        **kwargs,
    ):
        """
        :param answer: The answer provided by the LLM.
        :type answer: str
        :param created_at: The ISO date formatted timestamp of when the answer
                            to the prompt was created.
        :type created_at: str
        :param completion_reason: The reason the streamed response finishes.
        :type completion_reason: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.answer = answer
        self.created_at = created_at
        self.completion_reason = completion_reason


# Key value pair for metadata suggestion item
class IntelligenceMetadataSuggestionItem(BaseObject):
    def __init__(self, key: str, value: str, **kwargs):
        """
        :param key: The key of the metadata suggestion
        :type key: str
        :param value: The value of the metadata suggestion
        :type value: str
        """
        super().__init__(**kwargs)
        self.key = key
        self.value = value


# Suggestions as a dictionary of suggestion items
class IntelligenceMetadataSuggestions(BaseObject):
    def __init__(
        self,
        suggestions: Dict[str, IntelligenceMetadataSuggestionItem],
        **kwargs,
    ):
        """
        :param suggestions: The suggestions for the metadata
        :type suggestions: Dict[str, IntelligenceMetadataSuggestionItem]
        """
        super().__init__(**kwargs)
        self.suggestions = suggestions
