# syntax=docker/dockerfile:1.7
FROM python:3.11.13
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --upgrade pip
# RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN --mount=type=cache,target=/root/.cache/pip \
        pip install -r /code/requirements.txt
COPY ./app /code/app
COPY ./.env /code/.env
CMD ["fastapi", "run", "app/main.py", "--port", "80"]
