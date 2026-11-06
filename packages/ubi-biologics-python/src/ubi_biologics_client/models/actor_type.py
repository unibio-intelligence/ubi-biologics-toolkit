from enum import Enum


class ActorType(str, Enum):
    DELEGATED_AGENT = "delegated_agent"
    HUMAN = "human"
    INTEGRATION = "integration"
    SERVICE_AGENT = "service_agent"
    SYSTEM_WORKER = "system_worker"
    TOOL_CALLBACK = "tool_callback"

    def __str__(self) -> str:
        return str(self.value)
