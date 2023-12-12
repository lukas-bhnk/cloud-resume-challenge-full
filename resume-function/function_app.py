import json
import azure.functions as func
import logging
from azure.cosmos import CosmosClient
import os

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="resume_function")
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    endpoint = os.environ["COSMOS_DB_ENDPOINT"]
    key = os.environ["COSMOS_DB_KEY"]
    client = CosmosClient(endpoint, key)
    database_name = 'Resume'
    database = client.get_database_client(database_name)
    container_name = 'Items'
    container = database.get_container_client(container_name)

    query = "SELECT * FROM c"
    items = list(container.query_items(query=query, enable_cross_partition_query=True))

    if items:
        # Increment counter
        newCounter = items[0]['counter'] + 1
        items[0]['counter'] = newCounter

        # Replace the entire document in the database
        container.replace_item(item=items[0]['id'], body=items[0])

        # Create a JSON response with the updated counter
        response_body = json.dumps({"counter": newCounter})
        return func.HttpResponse(body=response_body, mimetype="application/json", status_code=200)
    else:
        return func.HttpResponse("No items found", status_code=404)
