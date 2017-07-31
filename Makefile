
.PHONY: archive publish

include config.mk

init_pyenv:
	pip install -r requirements.txt -t .

init_pyconf:
	echo "ELASTIC_URL = $(ELASTIC_URL)" > config.py
	echo "ELASTIC_INDEX = $(ELASTIC_INDEX)" >> config.py

archive: init_pyenv init_pyconf
	zip -9 archive.zip -r . --exclude *.git/*


publish: archive
	aws lambda create-function \
	--region $(REGION) \
	--function-name $(FUNCTION_NAME) \
	--zip-file fileb://archive.zip \
	--role arn:aws:iam::$(ACCOUNT_ID):role/lambda_serverless_curator \
	--handler es_store.lambda_handler \
        --vpc-config SubnetIds=$(SUBNETS),SecurityGroupIds=$(SEC_GROUPS) \
	--runtime python3.6 \
	--timeout $(TIMEOUT) \
	--memory-size $(MEMORY)
