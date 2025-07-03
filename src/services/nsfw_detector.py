from typing import Literal

import httpx
from pydantic import BaseModel
from pydantic import ValidationError
from fastapi import UploadFile

from core import exceptions
from services.logger import uvicorn_logger


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
            try:
                response = await client.post(
                    url=self.HOST_URL,
                    files={
                        "file": file.file.read(),
                    },
                )
            except httpx.ConnectTimeout:
                raise exceptions.NSFWDetectorServiceIsUnavailable()

            # XXX: Not handled non `OK` response
            # XXX: Possible error is RateLimit
            if response.status_code != 200:
                raise exceptions.NSFWDetectorServiceIsUnavailable()

            # XXX: Not handled non `json` response
            response_json = response.json()

            try:
                response_model = NSFWDetectorServiceResponse(**response_json)
            except ValidationError:
                uvicorn_logger.error(
                    "NSFWDetectorServiceResponseValidationError",
                    str(response_json),
                )
                raise exceptions.NSFWDetectorServiceMissingScore()

            return response_model.data.nsfw
