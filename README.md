```markdown
# dfmp

A small demo project to show a minimal Flask project managed by Poetry interacting with a MongoDB, both running in separate containers.

## Description

This barebones program is designed to:
- Run in a dedicated container.
- Operate a Flask server on port 4100.
- Connect to a separate container named `mongo-container` running a MongoDB instance on port 27017.

The Python project relies on Poetry for dependency management and is defined by the `pyproject.toml` file.

## API Endpoints

Flask will serve two API endpoints:
1. `store_string`: Accepts a string and stores it in the MongoDB backend.
2. `list_all_strings`: Retrieves and lists all stored strings from the backend.

## Running the Project

You can run the entire project from its root directory using the following command:
```
docker-compose up -d
```

## Testing

To test the project, use `curl` (or any other REST client) from the host running the container:
- Storing a string:
```
curl "http://localhost:12345/store?data=Ciao-Luffy"
```
- Listing all stored strings:
```
curl "http://localhost:12345/listall"
```

## Data Persistence

All data will be persistently stored under the `./data` directory on the host filesystem located at the project root.
```