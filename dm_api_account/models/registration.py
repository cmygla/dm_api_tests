from pydantic import (
    BaseModel,
    Field,
    ConfigDict,
)


class Registration(BaseModel):
    model_config = ConfigDict(extra="forbid")
    login: str = Field(..., description="Логин")  # обязательное поле
    password: str = Field(..., description="Пароль")
    email: str = Field(..., description="Емейл")
