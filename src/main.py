from typing import Annotated
from typing import Union

from pydantic import AfterValidator
from fastapi import FastAPI
from fastapi import UploadFile
from fastapi import File
from fastapi import status

from core import config
from core import dependencies
from core import schemas
from services.nsfw_detector import NSFWDetectorService


app = FastAPI(
    title="NSFW moderation service",
    summary="Сервис модерации изображений (`.jpg`, `.png`)",
    description="""
    Сервер, который принимает изображение и
    отправляет его в бесплатный сервис модерации,
    чтобы понять — есть ли на нём нежелательный контент
    """,
)


@app.post(
    "/moderate",
    tags=["moderation"],
    status_code=status.HTTP_200_OK,
    response_model=Union[
        schemas.ModerateResponseOK,
        schemas.ModerateResponseNSFWContent,
    ],
)
async def moderate(
    file: Annotated[
        UploadFile,
        AfterValidator(dependencies.moderate_file_validator),
        File(
            description="Файл для модерации: {}".format(
                config.SUPPORTED_FILE_EXT_VIEW,
            )
        ),
    ],
):
    """Проверка файла на нежелательный контент"""
    nsfw_score = await NSFWDetectorService().detect(file=file)

    if nsfw_score > config.NSFW_SCORE_MIN:
        return {
            "status": "REJECTED",
            "reason": "NSFW Content",
        }

    return {
        "status": "OK",
    }
