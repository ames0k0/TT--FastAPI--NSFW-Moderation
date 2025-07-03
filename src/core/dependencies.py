import os

from fastapi import UploadFile

from core import config
from core import exceptions


def moderate_file_validator(file: UploadFile) -> UploadFile:
    """Проверка расширение файла"""
    file_name = file.filename
    if not file_name:
        raise exceptions.MissingFileName()

    _, file_ext = os.path.splitext(file_name)
    if not file_ext:
        raise exceptions.MissingFileExtension()

    if file_ext not in config.SUPPORTED_FILE_EXT:
        raise exceptions.FileExtensionIsNotSupported(file_ext=file_ext)

    return file
