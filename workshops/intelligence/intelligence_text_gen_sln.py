"""Box Text Generation API example."""

import logging

from box_sdk_gen import AiDialogueHistory, AiResponse, BoxAPIError
from box_sdk_gen import BoxClient as Client
from box_sdk_gen import CreateAiAskItems

from utils.box_client_oauth import ConfigOAuth, get_client_oauth

logging.basicConfig(level=logging.INFO)
logging.getLogger("box_sdk_gen").setLevel(logging.CRITICAL)

DEMO_FILE = "1514587167701"


def text_gen(
    client: Client,
    prompt: str,
    file_id: str,
    content: str = None,
    dialogue_history: AiDialogueHistory = None,
) -> AiResponse:
    """Ask a question to the AI"""

    if file_id is None:
        raise ValueError("file_id must be provided")

    items = [CreateAiAskItems(id=file_id, type="file")]

    # add content if provided
    if content is not None:
        items[0]["content"] = content

    try:
        # response = client.intelligence.intelligence_text_gen(
        response = client.ai.create_ai_text_gen(
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
    client = get_client_oauth(conf)

    me = client.users.get_user_me()
    print(f"\nHello, I'm {me.name} ({me.login}) [{me.id}]")

    # Text gen dialog
    dialog_history = []
    while True:
        question = input("\nWhat would you like to talk about? (type 'exit' to quit): ")
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
            AiDialogueHistory(
                prompt=question,
                answer=response.answer,
                created_at=response.created_at,
            )
        )


if __name__ == "__main__":
    main()
