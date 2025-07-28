from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any

@dataclass
class SenderBehavior:
    _id: Optional[str]
    name: str          # Ex: "marketing_campaign", "transactional", "password_reset"
    provider: str      # Ex: "gmail", "sendgrid", "mailgun", "aws_ses"
    max_daily_limit: Optional[int] = 500 # 2000 # Limite de e-mails por dia para essa estratégia
    priority: int = 100 # Prioridade de envio (menor é mais prioritário)
    config: Dict[str, Any] = None # Configurações específicas do provedor (ex: API_KEY, FROM_EMAIL)
    is_active: bool = True

    def __post_init__(self):
        if self.config is None:
            self.config = {}

    def to_dict(self):
        return {k: v for k, v in asdict(self).items() if v is not None}

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=str(data.get("_id") or data.get("id")), # Suporta MongoDB (_id) e outros (id)
            name=data.get("name"),
            provider=data.get("provider"),
            max_daily_limit=data.get("max_daily_limit"),
            priority=data.get("priority"),
            config=data.get("config"),
            is_active=data.get("is_active", True)
        )
