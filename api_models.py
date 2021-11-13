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
import base64
import binascii

api = FastAPI(
    title="API Models",
    description="""This API allow to get predictions from trained
     Machine Learning models
    """,
    version="1.0.0",
)


credentials = [
    b"alice:wonderland",
    b"bob:builder",
    b"clementine:mandarine",
    b"admin:4dm1N",
]


model_files = glob.glob("*_trained")
models = {}

for file_model in model_files:
    with open(file_model, "rb") as mod_file:
        model = pickle.load(mod_file)

    models[type(model).__name__] = model


@api.get("/", name="Check API")
def index() -> dict:
    """
    Return a dictionnary that indicate the api is running
    """

    return {"status": "running"}


@api.get("/info", name="Get informations")
def get_info(
    authorization_header=Header(
        default="Basic ",
        description="""authorization header need to contain
    credentials of user (username:password)""",
    )
) -> dict:
    """
    Return informations on the API
    """
    if "Basic " not in authorization_header:
        raise HTTPException(
            status_code=400, detail="Invalid authorization header"
        )

    authorization_string = re.search("Basic .*", authorization_header)

    if authorization_string is None:
        authorization_bytes = None
    else:
        authorization_bytes = (
            authorization_string.group().split("Basic")[1].strip().encode()
        )

    try:
        authorization_decoded = base64.decodebytes(authorization_bytes)
    except (binascii.Error, TypeError):
        raise HTTPException(status_code=400, detail="Invalid base64 string")

    if (
        authorization_decoded is None
        or authorization_decoded not in credentials
    ):
        raise HTTPException(
            status_code=403,
            detail="You do not have authorization to acces this ressource",
        )

    # Return models list
    return {"models": list(models.keys())}
