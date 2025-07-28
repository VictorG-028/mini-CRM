from dataclasses import dataclass, asdict
from typing import Any, Literal

@dataclass
class Email:
    subject: str
    body: str # html_email

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]):
        return cls(
            sender=data["sender"],
            subject=data["subject"],
            body=data["body"]
        )
