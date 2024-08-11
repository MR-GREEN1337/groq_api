from contextlib import asynccontextmanager
from typing import Dict, List, Optional, Union
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from src.groq_client import get_models, inference_model

load_dotenv()


list_models = []  # Define list_models globally


@asynccontextmanager
async def lifespan(app: FastAPI):
    global list_models
    # Fetch the models during startup
    list_models = await get_models()

    # Yield to indicate that startup is complete
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def hello():
    return {"Hello": "There"}


@app.get("/inference")
async def inference_groq(
    prompt: str, model_name: Optional[Union[str, None]] = None
) -> List[Dict[str, str]]:
    global list_models

    if not model_name:
        inference_outputs = []
        for model in list_models:
            output = await inference_model(prompt=prompt, model_name=model)
            print(output)
            inference_outputs.append({model: output})

        return inference_outputs

    else:
        if model_name not in list_models:
            raise HTTPException(
                status_code=400, detail=f"Model '{model_name}' not found."
            )

        output = await inference_model(prompt=prompt, model_name=model_name)
        return [{model_name: output}]
