# pull official base image
FROM python:3.8-slim

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# set work directory
WORKDIR /app

COPY . /app/

# copy and run pipenv
COPY Pipfile* /app/
RUN pip install pipenv \
    && pipenv install --deploy --system --ignore-pipfile

# copy entrypoint.sh
COPY entrypoint.sh /app/
# make entrypoint.sh executable
RUN chmod +x ./entrypoint.sh

# run entrypoint.sh
CMD ./entrypoint.sh
