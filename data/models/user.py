from dataclasses import dataclass
from typing import Optional


@dataclass
class UserDB:
    user_login: str
    user_email: str
    display_name: Optional[str] = None
    last_name: Optional[str] = None

    @classmethod
    def from_db_row(cls, row: dict):
        return cls(
            user_login=row["user_login"],
            display_name=row.get("display_name"),
            user_email=row["user_email"],
            last_name=row.get("last_name")
        )
