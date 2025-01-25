from __future__ import annotations

from typing import Optional

from pydantic import (
    BaseModel,
    ConfigDict,
)


class ResetPassword(BaseModel):
    model_config = ConfigDict(extra="forbid")
    login: Optional[str] = None
    email: Optional[str] = None
