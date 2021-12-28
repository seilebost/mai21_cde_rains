FROM ubuntu:20.04

WORKDIR /train/

WORKDIR /tests/

WORKDIR /ml_models/ 

ADD requirements.txt api_models.py ./

ADD train/* train/

ADD tests/* tests/

ADD ml_models/* ml_models/

RUN apt update && apt install python3-pip -y && pip install -r requirements.txt

EXPOSE 8000

CMD uvicorn api_models:api --host 0.0.0.0

