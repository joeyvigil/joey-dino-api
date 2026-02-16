# Check dino_model for more detailed notes

from typing import Optional
from typing_extensions import Annotated
from pydantic import BaseModel, Field, SecretStr


class UserModel(BaseModel):
    id: Annotated[Optional[int], Field(gt=0)] = None
    username: Annotated[str, Field(min_length=3, max_length=50)]
    email: Annotated[str, Field(min_length=5, max_length=100)]
    password: Annotated[SecretStr, Field(min_length=8, max_length=100)]
    