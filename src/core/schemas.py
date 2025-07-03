from typing import Literal

from pydantic import BaseModel


class ModerateResponseOK(BaseModel):
    status: Literal["OK"]


class ModerateResponseNSFWContent(BaseModel):
    status: Literal["REJECTED"]
    reason: Literal["NSFW Content"]
