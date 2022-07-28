# list queues
aws --endpoint-url=http://localhost:4566 sns list-topics --profile test-profile

# add sns
aws --endpoint-url=http://localhost:4566 sns create-topic --name order-creation-events --region us-east-2 --profile test-profile --output table
# add queue
aws --endpoint-url=http://localhost:4566 sqs create-queue --queue-name dummy-queue --profile test-profile --region us-east-2 --output table