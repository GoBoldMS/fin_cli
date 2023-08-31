import abc
import typing
from typing import Any, Generic, TypeVar

from pydantic import BaseModel 


class SystemConfiguration(BaseModel):

    
    class Config:
        """Pydantic configuration."""
        extra = "forbid"
        env_file = ".env"
        env_file_encoding = "utf-8"



class SystemSettings(BaseModel):
    """A base class for all system settings."""

    name: str
    description: str

    class Config:
        extra = "forbid"
        use_enum_values = True
    
S = TypeVar("S", bound=SystemSettings)


class Configurable(abc.ABC, Generic[S]):
    """A base class for all configurable objects."""

    prefix: str = ""
    default_settings: typing.ClassVar[S]
    
    @classmethod
    def get_user_config(cls) -> S:
        """Get the user configuration."""
        return cls.default_settings.__class__(**cls.default_settings.dict())