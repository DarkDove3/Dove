# Create a new Chalice project called `lambda-dynamodb-example`
.PHONY: new
new: 
	chalice new-project lambda-dyanmodb-example

# Create a DynamoDB table from `resources.json` 
.PHONY: table
table:
	aws cloudformation deploy --template-file resources.json --stack-name devices-table

# Get the name of the DynamoDB table
.PHONY: table-info
table-info:
	aws dynamodb describe-table --table-name $(shell aws cloudformation describe-stacks --query "Stacks[0].Outputs[?OutputKey=='DevicesTableName'].OutputValue" --output text)

# Invoke the function locally
# Run `chalice local --port=8080` to run the function at localhost:8080
.PHONY: invoke-local
invoke-local: event
	curl -X PUT localhost:8080/insert -H "Content-Type:application/json" -d @event.json

# Invoke the deployed Lambda function through API Gateway
.PHONY: invoke-deployed
invoke-deployed: event
	curl -X PUT https://lraudwpaw6.execute-api.us-east-1.amazonaws.com/api/insert -H "Content-Type:application/json" -d @event.json

# Generate a new event before invoking the function
.PHONY: event
event:
	echo '{ "device_id": "$(shell uuidgen)" }' > event.json
