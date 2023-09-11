""" This barebones program is meant to run in a dedicated container
    running a Flask server on the 4100 port and connecting
    to a separate container named mongo-conainer running a mongodb instance on port 27017
    
    The python project is managed by poetry with its pyproject.toml file.
    
    Flask will be serving two API calls:
    store_string : will store the provided string in the mongodb backend
    list_all_strings : will list all stored strings from the backend
    and also
    apidocs : which will show the Swagger API documentation in a browser
    
    
    Run the whole project from the root with "docker-compose up -d"
    
    To test you can use curl (or any other REST interface) 
    from the same host running the container as follows:
    
    curl "http://localhost:12345/store?data=Ciao-Luffy"
    
    or
    
    curl "http://localhost:12345/listall"
    
    Data will persist under the ./data directory on the host filesystem under the project root
"""

import os
from flask import Flask, request, jsonify
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError, WriteError, ServerSelectionTimeoutError
from flasgger import Swagger


app = Flask(__name__)
swagger = Swagger(
    app
)  # to implement the apidocs endpoint; content from the functional endpoints docstrings

try:
    # Fetching environment variables; if unset give default value
    MONGO_HOSTNAME = os.environ.get('MONGODB_HOSTNAME', 'mongo-container')
    MONGO_DATABASE = os.environ.get('MONGODB_DATABASE', 'flasktest')
    MONGO_COLLECTION = os.environ.get('MONGODB_COLLECTION','storedstrings')

    # MongoDB setup
    client = MongoClient(
        f"mongodb://{MONGO_HOSTNAME}:27017/", serverSelectionTimeoutMS=5000
    )
    client.server_info()  # This will trigger a connection attempt or trigger the exception
    db = client[MONGO_DATABASE]  # database name from environment variable
    collection = db[MONGO_COLLECTION]  # collection name

except ServerSelectionTimeoutError as err:
    # Handle the exception and provide a user-friendly message
    app.logger.error("Could not connect to MongoDB: %s", err)
    client = None
    db = None
    collection = None


@app.route("/store", methods=["GET"])
def store_string():
    """will store the string in the mongodb backend collection
    ---
    parameters:
      - name: data
        in: query
        type: string
        required: true
        description: The string to store.
    responses:
      200:
        description: The result of the storage operation.
    """
    # Get the string from the URL parameter
    input_string = request.args.get("data")

    if input_string:
        try:
            # Store the string in the MongoDB collection
            result = collection.insert_one({"stored_string": input_string})
            if result.acknowledged:
                return "String stored successfully in MongoDB.\n"
            else:
                return "Insert operation not acknowledged by MongoDB.\n"
        except (DuplicateKeyError, WriteError) as mongoerr:
            return f"Failed to store the string in MongoDB: {str(mongoerr)}\n"
    else:
        return "No data provided in the URL.\n"


@app.route("/listall", methods=["GET"])
def list_all_strings():
    """will list stored strings from the backend collection
    ---
    responses:
      200:
        description: A list of stored strings.
        schema:
          type: array
          items:
            type: string
    """
    strings = collection.find({}, {"_id": 0, "stored_string": 1})
    stored_strings = [entry["stored_string"] for entry in strings]
    return jsonify(stored_strings)


if __name__ == "__main__":
    app.run(
        host="0.0.0.0", port=4100
    )  # 0.0.0.0 will accept connections from any interface not only loopback
