from fastapi import FastAPI, HTTPException, Header, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List
import re
import pandas as pd
import time
import datetime
from enum import Enum
import pickle
import glob

api = FastAPI(
    title='API Models',
    description=
    """This API allow to get predict from trained Machine Learning models
    """,
    version="1.0.0"
)


credentials = [
  "alice:wonderland",
  "bob:builder",
  "clementine:mandarine",
  "admin:4dm1N"
]


model_files = glob.glob("*_trained")
models = {}

for file_model in model_files:
    with open(file_model, 'rb') as mod_file:
        model = pickle.load(mod_file)

    models[type(model).__name__] = model

print(models.keys())

@api.get('/', name='Check API')
def index() -> dict:
    """
    Return a dictionnary that indicate the api is running
    """

    return {"status": "running"}

@api.get('/info', name='Get database informations for use and subject')
def get_info(authorization_header=Header(default="Basic ",
                                  description="authorization header need to contain credentials of user (username:password)")) -> dict:
    """
    Return a dictionnary that contains use and subjects values with their ids
    """

    authorization_string = re.search("Basic \w*:\w*",authorization_header)

    if authorization_string is None or authorization_string.group().split("Basic ")[1] not in credentials:
        raise HTTPException(status_code=403, detail="You do not have authorization to acces this ressource")

    return {"models": list(models.keys())}

    