# dfmp

A small demo project to show a minimal Flask project managed by Poetry interacting with a MongoDB, both running in separate containers orchestrated by Docker compose.

In some time I will try to expand it to this full architecture, with end user authentication based on JWT. 
![Component model](https://i.imgur.com/YcVQsQW.png)
For now only Flask, Gunicorn, MongoDB in two containers, orchestrated by Docker Compose is ready.

## Description

This barebones Flask program is designed to:
- Run in a dedicated container.
- Operate a Flask server on port 4100, exposing its port as 12345 on its host.
- Connect to a separate container named `mongo-container` (as defined in docker-compose.yml) running a MongoDB instance on port 27017, reachable only within the internal Docker network

The Python project relies on Poetry for python dependency management as defined by the `pyproject.toml` file.

## API Endpoints

The Flask app will serve three API endpoints:
1. `store`: Accepts a string and stores it in the MongoDB backend.
2. `list_all`: Retrieves and lists all stored strings from the backend.
3. `apidocs`: will show the Swagger interface in a browser to document/test the APIs

## Running the Project

You can run the entire project from its root directory using the following command:
```
docker compose up -d
```
on older docker versions the syntax could be 'docker-compose up  -d'

## Testing

To test the project, use `curl` (or any other REST client) from the same host running the project:
- Storing a string:
```
curl "http://localhost:12345/store?data=Isaac-Newton"
```
which of course can be repeated with other strings.

You can also use the small python utility provided in the additional directory (see below) to generate 500 random names.

- Listing all stored strings:
```
curl "http://localhost:12345/listall"
```

## Swagger APIs documentation

Pointing your browser to:
```
http://localhost:12345/apidocs
```
will let you explore and interact with the APIs Swaggero documentation implemented by flasgger in the endpoints docstrings.

## Data Persistence

All data will be persistently stored under the `./data` directory on the host filesystem located at the project root, so that if you
stop and later restart the container nothing will be lost.

## Additional

Under the additional directory you will find a small utility program which will generate 500 fake legit names and surnames
and will inject them into the MongoDB collectio. You can run it from within the additional directory as:
```
poetry run python fill500.py
```
but if you haven't already you must first also run the following command to satisfy the module 'requests' and 'faker' libraries:
```
poetry install requests faker
```
Please note that fill500.py is meant to be run as a client on the host, and will therefore not be copied into the container because of the content of the .gitignore file. If for any reason you wish to run it inside the container, remove additional/ 
from .gitignore and modify the Dockerfile removing the --no-dev options.

Enjoy!
