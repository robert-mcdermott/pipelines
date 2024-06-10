"""
title: Fred Hutch Code PHI
date: 2024-06-05
version: 1.0
license: MIT
description: A pipeline for filtering out PHI.
requirements: 
"""

from typing import List, Optional
from schemas import OpenAIChatMessage
from pydantic import BaseModel
from transformers import pipeline
import os


class Pipeline:
    class Valves(BaseModel):
        pipelines: List[str] = []
        priority: int = 0

    def __init__(self):
        self.type = "filter"
        self.name = "PHI Filter"

        # Initialize
        self.valves = self.Valves(
            **{
                "pipelines": ["*"],  # Connect to all pipelines
            }
        )
        self.model = None
        pass

    async def on_startup(self):
        # This function is called when the server is started.
        print(f"on_startup:{__name__}")

        self.model = pipeline("token-classification", model="obi/deid_roberta_i2b2")
        pass

    async def on_shutdown(self):
        # This function is called when the server is stopped.
        print(f"on_shutdown:{__name__}")
        pass

    async def on_valves_updated(self):
        # This function is called when the valves are updated.
        pass

    async def inlet(self, body: dict, user: Optional[dict] = None) -> dict:
        # This filter is applied to the form data before it is sent to the OpenAI API.
        print(f"inlet:{__name__}")

        print(body)
        user_message = body["messages"][-1]["content"]

        # Filter out toxic messages
        NER = []
        results = self.model(user_message)
        for res in results:
            if res['score'] > 0.9:
                NER.append(res)

        self.phi = "Clean"

        if len(NER) > 0:
            #raise Exception("""⚠️ PHI Decteted 🏥""")
            self.phi = "PHI detected"

        return body

    async def outlet(self, body: dict, user: dict) -> dict:
        # This function is called after the OpenAI API response is completed. You can modify the messages after they are received from the OpenAI API.
        print(f"outlet:{__name__}")
        body = self.phi
        print(body)
        print(user)

        return body
