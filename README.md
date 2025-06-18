# python-fastapi-lambda-sample

FastAPI example to deploy a small CRUD REST service in AWS Lambda. Data is stored in MongoDB using Beanie.

## Automatic tests

`make test`:
* starts a MongoDB docker instance
* runs pytest
* shuts down Mongo

Tests are running within a `dogs_test` database (on port 27018)

## Local manual run

A MongoDB `dogs` database must be ready on localhost:27017
You can start one with: `make mongo-up`

To start server: `make serve`

Tests:
```
curl http://localhost:8000/dogs
curl -X POST http://localhost:8000/dogs -d '{"name":"medor", "race":"golden retriever", "date_of_birth": "2022-11-11"}' -H "Content-Type: application/json"
curl http://localhost:8000/dogs/<id>
curl -X PUT http://localhost:8000/dogs/<id> -d '{"name":"Nelly", "race":"golden retriever", "date_of_birth": "2023-01-21"}' -H "Content-Type: application/json"
curl -X DELETE http://localhost:8000/dogs/<id>
```

## Serverless with AWS Lambda

The project uses Mangum to deploy FastAPI endpoints to AWS Lambda.
Deployment is managed by AWS SAM based on template.yml configuration.

To build the artifact for Lambda: `make build`
To test locally: `make serve-sam`
To deploy and run on AWS Lambda: `make deploy`