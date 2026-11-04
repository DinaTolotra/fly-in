from pydantic import BaseModel, Field
from typing import Annotated, Optional
from enum import Enum
from math import inf


class HubRole(Enum):
    HUB = "hub"
    START = "start_hub"
    END = "end_hub"


class HubType(Enum):
    PRIORITY = "priority"
    NORMAL = "normal"
    RESTRICTED = "restricted"
    BLOCKED = "blocked"

    @property
    def priority(self) -> float:
        if self == HubType.PRIORITY:
            return 0.
        elif self == HubType.NORMAL:
            return 1.
        elif self == HubType.RESTRICTED:
            return 2.
        elif self == HubType.BLOCKED:
            return inf
        else:
            raise ValueError(f"Unknown hub type: {self}")

    @property
    def cost(self) -> float:
        if self == HubType.PRIORITY:
            return 1.
        elif self == HubType.NORMAL:
            return 1.
        elif self == HubType.RESTRICTED:
            return 2.
        elif self == HubType.BLOCKED:
            return inf
        else:
            raise ValueError(f"Unknown hub type: {self}")


class Hub(BaseModel):
    hub_role: Annotated[HubRole, Field(default=HubRole.HUB)]
    hub_name: Annotated[str, Field(pattern="^[a-zA-Z0-9_]+$")]
    position: Annotated[tuple[float, float], Field()]
    type: Annotated[HubType, Field(default=HubType.NORMAL)]
    color: Annotated[
        Optional[str],
        Field(default=None, pattern="^[a-zA-Z0-9]+$")
    ]
    max_drone: Annotated[int, Field(default=1, ge=1)]


class Connection(BaseModel):
    first: Annotated[Hub, Field()]
    second: Annotated[Hub, Field()]
    max_link_capacity: Annotated[int, Field(default=1, ge=1)]
