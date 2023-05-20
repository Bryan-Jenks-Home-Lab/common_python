# TODO flesh out a pushover class that is used for common purposes to send notifs for other apps

import datetime
import time
from dataclasses import dataclass, field
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

    def send_notification(self):
        """Send a pushover notification using the Pushover API"""
        url = "https://api.pushover.net/1/messages.json"
        data = self.__dict__
        return requests.post(url, data)
