from fastapi import status
from fastapi.exceptions import HTTPException

from core import config


class MissingFileName(HTTPException):
    def __init__(self):
        self.status_code: int = status.HTTP_400_BAD_REQUEST
        self.detail: str = "Отсутствует название файла"


class MissingFileExtension(HTTPException):
    def __init__(self):
        self.status_code: int = status.HTTP_400_BAD_REQUEST
        self.detail: str = "Отсутствует расширение файла: {}".format(
            config.SUPPORTED_FILE_EXT_VIEW
        )


class FileExtensionIsNotSupported(HTTPException):
    def __init__(self, *, file_ext: str):
        self.status_code: int = status.HTTP_400_BAD_REQUEST
        self.detail: str = "Расширение файла `{}` не поддерживает".format(
            file_ext,
        )


class NSFWDetectorServiceIsUnavailable(HTTPException):
    def __init__(self):
        self.status_code: int = status.HTTP_503_SERVICE_UNAVAILABLE
        self.detail: str = "NSFWDetectorService is unavailable"


class NSFWDetectorServiceMissingScore(HTTPException):
    def __init__(self):
        self.status_code: int = status.HTTP_503_SERVICE_UNAVAILABLE
        self.detail: str = "NSFWDetectorService: Missing `nsfw` score"
