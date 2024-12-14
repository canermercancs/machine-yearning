import pickle
import numpy as np
from pathlib import Path
from typing import Any
from pydantic import BaseModel, Field


class MockContainer(BaseModel):
    """
    Mock Model container class
    """

    model_name: str = Field("", description="Model name")
    model: Any = Field(None, description="Model")
    model_path: Path = Field(Path("models"), description="Full path of the Model")
    ext: str = ".pkl"

    class MockModel(BaseModel):
        def predict(self, data: Any):
            return int(np.random.random()>.5)
        
    def load(self, path: Path):
        """
        load the model from given path
        """
        self.model = self.MockModel()
        return True
        
    def download(self):
        # download a model from a model registry
        pass


class ModelContainer(BaseModel):
    """
    Model container class
    """

    model_name: str = Field("", description="Model name")
    model: Any = Field(None, description="Model")
    model_path: Path = Field(Path("models"), description="Full path of the Model")
    ext: str = ".pkl"

    def load(self, path: Path):
        """
        load the model from given path
        """
        model_path = [item for item in path.glob("*") if self.model_name in item.stem]
        if len(model_path) != 1:
            return False
        
        self.model_path = model_path[0].resolve()
        with open(self.model_path, "rb") as f:
            self.model = pickle.load(f)
        return True
        

    def download(self):
        # download a model from a model registry
        pass