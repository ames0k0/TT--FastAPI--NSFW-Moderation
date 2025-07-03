from typing import Sequence


SUPPORTED_FILE_EXT: Sequence[str] = (
    ".jpg",
    ".png",
)
SUPPORTED_FILE_EXT_VIEW: str = " | ".join(SUPPORTED_FILE_EXT)
NSFW_SCORE_MIN: float = 0.7
