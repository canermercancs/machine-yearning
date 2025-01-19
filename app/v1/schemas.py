from typing import Any
from pydantic import BaseModel, Field


class HealthSchema(BaseModel):
    """
    Health model for the health check of model API.
    """

    status: str = Field(
        ..., description="Status of the health check", examples=["healthy"]
    )
    version: str = Field(..., description="Version of the model API", examples=["0.0.1"])
    model_name: str | None = Field(..., description="Name of the model")


class InputSchema(BaseModel):
    """
    Model input request.
    """

    data: Any = Field(..., description="Input Data")


class ModelResponseSchema(BaseModel):
    """
    Model response.
    """

    prediction: Any = Field(..., description="List of binary predictions.")
