"""
title: Fred Hutch Code of PHI Filter
date: 2024-06-07
version: 1.0
license: MIT
description: A pipeline for stopping the use of PHI.
requirements: requests
"""

from typing import List, Optional
from pydantic import BaseModel
from schemas import OpenAIChatMessage


class Pipeline:
    class Valves(BaseModel):
        pipelines: List[str] = []
        priority: int = 0
        pass

    def __init__(self):
        self.type = "filter"
        self.name = "Filter"
        self.valves = self.Valves(**{"pipelines": ["llama3:latest"]})
        pass

    async def on_startup(self):
        print(f"on_startup:{__name__}")
        pass

    async def on_shutdown(self):
        print(f"on_shutdown:{__name__}")
        pass

    async def inlet(self, body: dict, user: Optional[dict] = None) -> dict:
        print(f"inlet:{__name__}")
        print(body)
        user_message = body["messages"][-1]["content"]

        # Filter out PHI
        toxicity = self.model.predict(user_message)
        print(toxicity)

        if toxicity["toxicity"] > 0.5:
            raise Exception("""⚠  Your prompt violates Fred Hutch's standards of conduct.
                               💣 Repeated violations may result in loss of system access or other actions.
                               👉 Review the standards here https://centernet.fredhutch.org/u/compliance-office/standards.html""")

        return body
