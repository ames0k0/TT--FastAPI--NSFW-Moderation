import os
from typing import Annotated
from typing import Sequence
from typing import Literal

import httpx
from pydantic import BaseModel
from pydantic import ValidationError
from fastapi import FastAPI
from fastapi import UploadFile
from fastapi import File
from fastapi import status
from fastapi.exceptions import HTTPException


app = FastAPI(
    title="NSFW moderation service",
    summary="Сервис модерации изображений (`.jpg`, `.png`)",
    description="""
    Сервер, который принимает изображение и
    отправляет его в бесплатный сервис модерации,
    чтобы понять — есть ли на нём нежелательный контент
    """,
)


SUPPORTED_FILE_EXT: Sequence[str] = (
    ".jpg",
    ".png",
)
SUPPORTED_FILE_EXT_VIEW: str = " | ".join(SUPPORTED_FILE_EXT)
NSFW_SCORE_MIN: float = 0.7


class ModerateResponseOK(BaseModel):
    status: Literal["OK"]


class ModerateResponseNotOK(BaseModel):
    status: Literal["REJECTED"]
    reason: Literal["NSFW Content"]


class NSFWDetectorServiceResult(BaseModel):
    normal: float
    nsfw: float


class NSFWDetectorServiceResponse(BaseModel):
    data: NSFWDetectorServiceResult
    status: Literal[1]


class NSFWDetectorService:
    """NSFW Detector Service

    Docs: https://github.com/tmplink/nsfw_detector
    """

    HOST_URL: str = "https://vx.link/public/nsfw"

    async def detect(self, file: UploadFile) -> float:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url=self.HOST_URL,
                files={
                    "file": file.file.read(),
                },
            )

            try:
                response = NSFWDetectorServiceResponse(**response.json())
            except ValidationError:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="NSFWDetectorService: Missing `nsfw` score",
                )

            return response.data.nsfw


@app.post(
    "/moderate",
    tags=["moderation"],
    status_code=status.HTTP_200_OK,
    response_model=ModerateResponseOK | ModerateResponseNotOK,
)
async def moderate(
    file: Annotated[
        UploadFile,
        File(description=f"Файл для модерации: {SUPPORTED_FILE_EXT_VIEW}"),
    ],
):
    file_name = file.filename
    if not file_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Отсутствует название файла",
        )

    _, file_ext = os.path.splitext(file_name)
    if file_ext not in SUPPORTED_FILE_EXT:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Поддерживает расширений файла: {SUPPORTED_FILE_EXT_VIEW}",
        )

    nsfw_score = await NSFWDetectorService().detect(file=file)

    if nsfw_score > NSFW_SCORE_MIN:
        return {
            "status": "REJECTED",
            "reason": "NSFW Content",
        }

    return {
        "status": "OK",
    }
