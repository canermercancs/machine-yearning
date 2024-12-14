import os
from constants import DEBUG_MODE
from pathlib import Path
from contextlib import asynccontextmanager
from typing import Any
from collections.abc import AsyncGenerator
from fastapi import FastAPI, HTTPException, status
from schemas import Healthy, InputRequest, ModelResponse
from classes import ModelContainer, MockContainer

if DEBUG_MODE:
    MODEL_CONTAINER = MockContainer()
else:
    MODEL_CONTAINER = ModelContainer()

# # Variables set during API startup
# MODEL = {}
# cols = ['claim_amount_claimed_total', 'claim_causetype', 'claim_date_occurred', 'claim_date_reported',
#         'claim_location_urban_area', 'object_make', 'object_year_construction', 'ph_gender', 'policy_fleet_flag',
#         'policy_insured_amount', 'policy_profitability']


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


@app.get("/health", response_model=Healthy)
def health() -> dict[str, str]:
    """
    Health check endpoint to see if API is running.

    :return: Healthy status and version.
    """

    if not MODEL_CONTAINER.model:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Cannot find the model!"
        )
    return dict(status="healthy", model_name=MODEL_CONTAINER.model_name, version="0.0.1")


@app.post("/predict", response_model=ModelResponse)
async def predict(request: InputRequest) -> dict[str, Any]:
    """
    Predict endpoint for model.
    """
    data = request.data
    ## TRANSFORM DATA
    ...

    model = MODEL_CONTAINER.model

    return {"prediction": model.predict(data)}    


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("run:app", host="0.0.0.0", port=8080) # , reload=bool(os.getenv("DEBUG")))
