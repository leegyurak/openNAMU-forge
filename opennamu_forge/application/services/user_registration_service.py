from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Protocol


class UserRegistrationUserSettings(Protocol):
    def has_any(self) -> bool: ...
    def add(self, user_id: str, name: str, data: str) -> None: ...


class UserRegistrationOtherSettings(Protocol):
    def get(self, name: str, *, coverage: str = "", default: str = "") -> str: ...


@dataclass(frozen=True)
class UserRegistrationService:
    user_settings: UserRegistrationUserSettings
    other_settings: UserRegistrationOtherSettings
    password_hasher: Callable[[str], str]
    now_provider: Callable[[], str]

    def add_user(self, user_name: str, user_pw: str, user_email: str = "", user_encode: str = "") -> None:
        if user_encode == "":
            user_pw_hash = self.password_hasher(user_pw)
            data_encode = self.other_settings.get("encode", default="sha3")
        else:
            user_pw_hash = user_pw
            data_encode = user_encode

        user_auth = "owner" if not self.user_settings.has_any() else "user"

        self.user_settings.add(user_name, "pw", user_pw_hash)
        self.user_settings.add(user_name, "acl", user_auth)
        self.user_settings.add(user_name, "date", self.now_provider())
        self.user_settings.add(user_name, "encode", data_encode)

        if user_email != "":
            self.user_settings.add(user_name, "email", user_email)
