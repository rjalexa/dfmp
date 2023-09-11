# Use an official Python runtime as a parent image
FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.6.1

# Install poetry
RUN pip install "poetry==$POETRY_VERSION" && \
    poetry config virtualenvs.create false
    
# Set the working directory to /app
WORKDIR /app

# Copy in the python prereq files:
COPY ./pyproject.toml ./poetry.lock /app/
# Install only python dependencies (skipping dev libraries):
RUN poetry install --no-root --no-dev

# Copy in everything else and install, this way if code changes the 
# packages layer will remain untouched,  (skipping dev libraries)
COPY . /app/
RUN poetry install --no-dev

# Use poetry to run app/app.py behind gunicorn
CMD ["poetry", "run", "gunicorn", "app.app:app", "-b", "0.0.0.0:4100", "--workers=4"]

