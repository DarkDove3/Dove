import boto3
from chalice import Chalice
from chalicelib.db import DevicesTable

# Replace this with the name of your table. Run `make table` to generate a table with CloudFormation
table_name = 'devices-table-DevicesTable-17L3QXQ7ZRCU6'

# Create a new Chalice instance
app = Chalice(app_name='lambda-dyanmodb-example')

# Use boto3 to get an AWS API object that has methods which let us interact with our DynamoDB table
table_resource = boto3.resource('dynamodb').Table(table_name)

# Use the table resource in our class
dynamo_client = DevicesTable(table_resource)

# Handler is the entrypoint to our Lambda function
# Make a PUT request to the /insert path with the header Content-Type:application/json set 
@app.route('/insert', methods=['PUT'], content_types=['application/json'])
def handler():
    # Extract event from request proxied by API Gateway
    event = app.current_request.json_body
    print(f"Inserting {event} into table {table_name}")

    # Insert the JSON into the DynamoDB Table
    # TODO: Retry logic if an error is returned
    error = dynamo_client.insert_device(event)

    # Return error to client if there was an error
    if error:
        return {'error': str(error)}
    
    # Return success message to client if it worked
    return {'status': 'Successfully inserted device into table'}
