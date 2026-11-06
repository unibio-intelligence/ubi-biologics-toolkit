from enum import Enum


class ProjectProfile(str, Enum):
    LEAD_DEVELOPMENT = "lead_development"
    REGULATED_DECISION = "regulated_decision"
    RESEARCH = "research"

    def __str__(self) -> str:
        return str(self.value)
