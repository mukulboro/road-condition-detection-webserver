FROM python:3.9


WORKDIR /code


COPY ./requirements.txt /code/requirements.txt

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 libgl1 -y
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app
COPY ./app/model.pt /code
COPY ./app/out_images /code



CMD [ "uvicorn", "app.server:app", "--host", "0.0.0.0", "--port", "80" ]