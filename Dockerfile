# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory to /app
WORKDIR /app

# Install poetry: Could be good to pin it to known release
RUN pip install poetry

# Copy in the python prereq files:
COPY pyproject.toml poetry.lock ./
# Install only python dependencies (skipping dev libraries):
RUN poetry install --no-root --no-dev

# Copy in everything else and install, this way if code changes the 
# packages layer will remain untouched,  (skipping dev libraries)
COPY . .
RUN poetry install --no-dev

# Make port 4100 available to the world outside this container
EXPOSE 4100
# Define environment variable ... not sure this is really needed
ENV NAME FlaskApp
# Run app.py  under poetry when the container launches
CMD ["poetry", "run", "python", "app/app.py"]

