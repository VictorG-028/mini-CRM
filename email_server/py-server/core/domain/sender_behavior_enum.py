from enum import StrEnum

class SenderBehaviorEnum(StrEnum):
    NOT_DEFINED = "not_defined"
    BY_BIRTHDAY = "by_birthday"
    LOW_CHANCE = "low_chance"
    MODERATE_CHANCE = "moderate_chance"
    HIGH_CHANCE = "high_chance"
