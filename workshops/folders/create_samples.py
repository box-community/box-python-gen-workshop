"""Uploads or Creates samples for exercises."""

import logging

from box_sdk_gen.client import BoxClient as Client
from utils.box_utils import create_box_folder, folder_upload


logging.getLogger(__name__)


def create_samples(client: Client):
    """Uploads sample content to Box."""
    wks_folder = create_box_folder(
        client, "workshops", client.folders.get_folder_by_id("0")
    )

    create_box_folder(client, "folders", wks_folder)
