import logging

from box_sdk_gen import BoxClient, CreateDocgenTemplateFile, DocgenTags, DocgenTemplate

from utils.box_client_oauth import ConfigOAuth, get_client_oauth

logging.basicConfig(level=logging.INFO)
logging.getLogger("box_sdk_gen").setLevel(logging.CRITICAL)

LEASE_TEMPLATE_ID = "1744637428174"


def mark_file_as_doc_gen_template(client: BoxClient, file_id: str) -> DocgenTemplate:
    """Mark a file as a DocGen template"""
    # check if file exists and it is accessible
    file = client.files.get_file_by_id(file_id)

    template_base = client.doc_gen_template.create_docgen_template(file=CreateDocgenTemplateFile(id=file.id))
    return client.doc_gen_template.get_docgen_template_by_id(template_base.file.id)


def get_tags_from_template(client: BoxClient, template_id: str) -> DocgenTags:
    """Get tags from a template"""
    return client.doc_gen_template.get_docgen_template_tags(template_id)


def main():
    """Simple script to demonstrate how to use the Box SDK"""
    conf = ConfigOAuth()
    client = get_client_oauth(conf)

    me = client.users.get_user_me()
    print(f"\nHello, I'm {me.name} ({me.login}) [{me.id}]")
    print("-" * 50)
    print()

    # Set the MS Word file as a doc gen template
    template = mark_file_as_doc_gen_template(client, LEASE_TEMPLATE_ID)
    print(f"Template created: {template.to_dict()}")

    # List template tags
    template_tags = get_tags_from_template(client, template.file.id)
    print("\nFound tags:")
    for tag in template_tags.entries:
        print(f"  - {tag.tag_content} : {tag.tag_type.name} : {tag.json_paths}")


if __name__ == "__main__":
    main()
