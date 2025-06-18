APP_NAME := python-fastapi-lambda-example
STACK_NAME := $(APP_NAME)-stack
REGION := eu-west-3
S3_BUCKET := python-fastapi-lambda-example-deploy-bucket
PROFILE := default

.PHONY: help build export deploy serve serve-sam test test-clean mongo-up mongo-down clean delete

help:
	@echo "Available Commands:"
	@echo "  make help         - Show this help message"
	@echo "  make test         - Run tests with pytest (with automated MongoDB container)"
	@echo "  make test-clean   - Stop MongoDB test container if still running"
	@echo "  make mongo-up     - Start MongoDB container for main app"
	@echo "  make mongo-down   - Stop MongoDB container for main app"
	@echo "  make serve        - Start local API server using Poetry/Uvicorn"
	@echo "  make serve-sam    - Start local API with SAM"
	@echo "  make export-deps  - export dependencies (requirements.txt)"
	@echo "  make build        - SAM build"
	@echo "  make deploy       - SAM deploy (interactive on 1st time)"
	@echo "  make delete       - Delete CloudFormation stack"
	@echo "  make clean        - Clean up generated files"

test:
	docker-compose up -d mongo-test
	sleep 3  
	poetry run pytest
	docker-compose stop mongo-test

test-clean:
	docker-compose stop mongo-test

mongo-up:
	docker-compose up -d mongo-main

mongo-down:
	docker-compose stop mongo-main

serve:
	poetry run uvicorn app.main:app --reload

export-deps:
	poetry export -f requirements.txt --without-hashes > requirements.txt

build: export-deps    # depends on export task to ensure requirements.txt is up-to-date
	sam build --use-container

serve-sam: export-deps   
	sam local start-api --env-vars .env-local-sam.json --docker-network python-fastapi-example_default

deploy:
	sam deploy \         # add --guided flag for interactive setup on first deployment
		--stack-name $(STACK_NAME) \
		--region $(REGION) \
		--s3-bucket $(S3_BUCKET) \
		--capabilities CAPABILITY_IAM \
		--profile $(PROFILE)

delete:
	sam delete --stack-name $(STACK_NAME) --region $(REGION)

clean:
	rm -rf .aws-sam requirements.txt __pycache__ .pytest_cache local-db-data/* tmp/*
