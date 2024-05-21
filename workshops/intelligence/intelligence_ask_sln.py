"""Box AI Client - Ask a question to the AI"""

import logging

from box_sdk_gen.client import BoxClient as Client

from box_sdk_gen import BoxAPIError
from box_sdk_gen.client import BoxClient as Client
from box_sdk_gen.managers.ai import CreateAiAskMode, CreateAiAskItems, AiResponse

from utils.box_client_oauth import ConfigOAuth, get_client_oauth


logging.basicConfig(level=logging.INFO)
logging.getLogger("box_sdk_gen").setLevel(logging.CRITICAL)

DEMO_FILE = "1530265998769"


def ask(client: Client, question: str, file_id: str, content: str = None) -> AiResponse:
    """Ask a question to the AI"""

    if file_id is None:
        raise ValueError("file_id must be provided")

    mode = CreateAiAskMode.SINGLE_ITEM_QA

    items = [CreateAiAskItems(id=file_id, type="file")]

    # add content if provided
    if content is not None:
        items[0]["content"] = content

    try:
        ai_response = client.ai.create_ai_ask(mode=mode, prompt=question, items=items)

    except BoxAPIError as e:
        print(f"Error: {e}")

    return ai_response


def main():
    """Simple script to demonstrate how to use the Box SDK"""
    conf = ConfigOAuth()
    client = get_client_oauth(conf)

    me = client.users.get_user_me()
    print(f"\nHello, I'm {me.name} ({me.login}) [{me.id}]")

    # Summarize the file
    response = ask(
        client,
        "Summarize document.",
        DEMO_FILE,
    )
    print(f"\nResponse: {response.answer}")

    while True:
        question = input("\nAsk a question (type 'exit' to quit): ")
        if question == "exit":
            break
        response = ask(
            client,
            question,
            DEMO_FILE,
        )
        print(f"\nResponse: {response.answer}")


if __name__ == "__main__":
    main()
