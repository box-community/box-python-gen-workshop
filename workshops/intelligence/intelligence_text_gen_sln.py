"""Box Text Generation API example."""

import logging

from utils.box_ai_client import BoxAIClient as Client

from box_sdk_gen.errors import BoxAPIError

from utils.ai_schemas import (
    IntelligenceResponse,
    IntelligenceDialogueHistory,
)


from utils.box_ai_client_oauth import ConfigOAuth, get_ai_client_oauth


logging.basicConfig(level=logging.INFO)
logging.getLogger("box_sdk_gen").setLevel(logging.CRITICAL)

DEMO_FILE = "1442379637774"


def text_gen(
    client: Client,
    prompt: str,
    file_id: str,
    content: str = None,
    dialogue_history: IntelligenceDialogueHistory = None,
) -> IntelligenceResponse:
    """Ask a question to the AI"""

    if file_id is None:
        raise ValueError("file_id must be provided")

    items = [{"id": file_id, "type": "file"}]

    # add content if provided
    if content is not None:
        items[0]["content"] = content

    try:
        response = client.intelligence.intelligence_text_gen(
            prompt=prompt,
            items=items,
            dialogue_history=dialogue_history,
        )
    except BoxAPIError as e:
        print(f"Error: {e}")

    return response


def main():
    """Simple script to demonstrate how to use the Box SDK"""
    conf = ConfigOAuth()
    client = get_ai_client_oauth(conf)

    me = client.users.get_user_me()
    print(f"\nHello, I'm {me.name} ({me.login}) [{me.id}]")

    # Text gen dialog
    dialog_history = []
    while True:
        question = input(
            "\nWhat would you like to talk about? (type 'exit' to quit): "
        )
        if question == "exit":
            break

        response = text_gen(
            client,
            question,
            DEMO_FILE,
            dialogue_history=dialog_history,
        )
        print(f"\nResponse: {response.answer}")

        dialog_history.append(
            IntelligenceDialogueHistory(
                prompt=question,
                answer=response.answer,
                created_at=response.created_at,
            )
        )


if __name__ == "__main__":
    main()
