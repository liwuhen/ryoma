from typing import Optional

import reflex as rx
from sqlmodel import Field

from ryoma.models.agent import AgentType


class Agent(rx.Model, table=True):
    id: Optional[str] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str]
    type: Optional[AgentType] = Field(default=AgentType.ryoma)
    workflow: Optional[str]