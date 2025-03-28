from constants import DEBUG_MODE
from pathlib import Path
from contextlib import asynccontextmanager
from typing import Any
from collections.abc import AsyncGenerator
from fastapi import FastAPI, HTTPException, status
from schemas import HealthSchema, InputSchema, ModelResponseSchema
from classes import ModelContainer, MockContainer

if DEBUG_MODE:
    MODEL_CONTAINER = MockContainer()
else:
    MODEL_CONTAINER = ModelContainer()

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Context manager to run startup and shutdown events for FastAPI app.

    :param app: FastAPI app, required argument for the decorator.
    """

    ### LOAD THE MODEL HERE.

    MODEL_CONTAINER.model_name = "caner_model"
    model_flag = MODEL_CONTAINER.load(path=Path("models"))

    if not model_flag:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Model loading failed!"
        )

    yield


# Initiate serving server
app = FastAPI(title="Caner's Custom Model", lifespan=lifespan)


@app.get("/health", response_model=HealthSchema)
def health() -> dict[str, str]:
    """
    Health check endpoint to see if API is running.

    :return: HealthSchema status and version.
    """

    if not MODEL_CONTAINER.model:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Cannot find the model!"
        )
    return dict(status="HealthSchema", model_name=MODEL_CONTAINER.model_name, version="0.0.1")


@app.post("/predict", response_model=ModelResponseSchema)
async def predict(request: InputSchema) -> dict[str, Any]:
    """
    Predict endpoint for model.
    """
    data = request.data
    ## TRANSFORM DATA
    ...

    model = MODEL_CONTAINER.model

    return {"prediction": model.predict(data)}    

