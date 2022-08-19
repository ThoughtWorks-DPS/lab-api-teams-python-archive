#!/bin/sh
set -ex

BASE_DIR="$(dirname $0)/.."

export $(cat ${BASE_DIR}/local/local.env | xargs)

localhost="--endpoint-url ${DYNAMODB_URL}"

if aws dynamodb describe-table ${localhost} --table-name ${DYNAMODB_TABLE_NAME} > /dev/null 2>&1; then
    echo "Table: ${DYNAMODB_TABLE_NAME} already exists..."
else
    echo "Creating table...: ${DYNAMODB_TABLE_NAME}"
    aws dynamodb create-table --table-name ${DYNAMODB_TABLE_NAME} ${localhost} --cli-input-json file://${BASE_DIR}/dynamodb_table_schema.json
    echo "${DYNAMODB_TABLE_NAME} has been created..."
fi

exec "$@"
