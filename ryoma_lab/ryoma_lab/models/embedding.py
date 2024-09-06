from typing import Optional, Any

import reflex as rx


class Embedding(rx.Base):
    model: str
    model_parameters: Optional[dict[str, Optional[Any]]] = None
