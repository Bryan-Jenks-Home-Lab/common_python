import base64
import datetime
import time
from dataclasses import dataclass
from enum import Enum

import requests
from pydantic import AnyUrl


class AttachmentFileTypes(str, Enum):
    JPEG = "image/jpeg"
    JPG = "image/jpeg"
    PNG = "image/png"
    BMP = "image/bmp"
    TIFF = "image/tiff"


@dataclass
class Pushover:
    """API documentation for this service can be found here: https://pushover.net/api"""

    token: str
    user: str
    title: str
    message: str
    html: int = 1
    sound: str = "falling"
    timestamp: float = time.mktime(datetime.datetime.now().timetuple())
    priority: int = 0
    retry: int = 30
    expire: int = 600
    url: AnyUrl = None
    url_title: str = None
    attachment_name: str = None
    attachment: bytes = None

    def __post_init__(self):
        if self.attachment_name:
            file_ext = self.attachment_name.split(".")[-1].upper()
            conditions_are_true = [
                self.attachment_name is not None,
                self.attachment is not None,
                hasattr(AttachmentFileTypes, file_ext),
            ]

            if all(conditions_are_true):
                file_attachment = {
                    "attachment": (
                        self.attachment_name,
                        base64.b64decode(self.attachment),
                        file_ext,
                    )
                }
        self.files = file_attachment if self.attachment_name is not None else None

    def send_notification(self):
        """Send a pushover notification using the Pushover API"""
        url = "https://api.pushover.net/1/messages.json"
        data = self.__dict__
        data.pop("attachment")
        return requests.post(url, data, self.files)
