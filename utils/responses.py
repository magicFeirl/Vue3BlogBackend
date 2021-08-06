from typing import Optional, Any
from pydantic import BaseModel


class BaseResponse(BaseModel):
    code: int
    message: str
    data: Optional[Any] = None
