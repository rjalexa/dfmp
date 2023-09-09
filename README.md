# dfmp

A small demo project to show a minimal Flask project managed by Poetry interacting with a MongoDB, both running in separate containers, orchestrated by Docker compose.

## Description

This barebones Flask program is designed to:
- Run in a dedicated container.
- Operate a Flask server on port 4100, exposing the port on its host.
- Connect to a separate container named `mongo-container` running a MongoDB instance on port 27017, only within the internal Docker network

The Python project relies on Poetry for dependency management as defined by the `pyproject.toml` file.

## API Endpoints

The Flask app will serve two API endpoints:
1. `store_string`: Accepts a string and stores it in the MongoDB backend.
2. `list_all_strings`: Retrieves and lists all stored strings from the backend.

## Running the Project

You can run the entire project from its root directory using the following command:
```
docker-compose up -d
```
on older docker versions the syntax could be 'docker compose up  -d'

## Testing

To test the project, use `curl` (or any other REST client) from the same host running the project:
- Storing a string:
```
curl "http://localhost:12345/store?data=Isaac-Newton"
```
which of course can be repeated with other strings.

- Listing all stored strings:
```
curl "http://localhost:12345/listall"
```

## Data Persistence

All data will be persistently stored under the `./data` directory on the host filesystem located at the project root.
