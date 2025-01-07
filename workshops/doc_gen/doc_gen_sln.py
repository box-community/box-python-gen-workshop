import logging

from utils.box_client_oauth import ConfigOAuth, get_client_oauth

from box_sdk_gen import DocgenTemplates, DocgenTemplate

logging.basicConfig(level=logging.INFO)
logging.getLogger("box_sdk_gen").setLevel(logging.CRITICAL)


def main():
    """Simple script to demonstrate how to use the Box SDK"""
    conf = ConfigOAuth()
    client = get_client_oauth(conf)

    me = client.users.get_user_me()
    print(f"\nHello, I'm {me.name} ({me.login}) [{me.id}]")
    print("-" * 50)
    print()

    items = client.folders.get_folder_items("0")
    for item in items.entries:
        print(f"  {item.name} [{item.id}]")

    doc_gen_templates: DocgenTemplates = client.doc_gen_template.get_docgen_templates()

    print("Docgen Templates:")
    for doc_gen_template in doc_gen_templates.entries:
        print(f"  {doc_gen_template.to_dict()}")


if __name__ == "__main__":
    main()
