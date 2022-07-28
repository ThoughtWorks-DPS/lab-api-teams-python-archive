import logging
import boto3
from botocore.exceptions import ClientError
import json

AWS_REGION = "us-east-2"
AWS_PROFILE = "test-profile"
boto3.setup_default_session(profile_name=AWS_PROFILE)

endpoint_url = "http://localhost:4566"
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s: %(levelname)s: %(message)s')

client = boto3.client("sns", endpoint_url=endpoint_url, region_name=AWS_REGION)


def create_topic(name):
    """
    Creates a SNS notification topic.
    """
    try:
        topic = client.create_topic(Name=name)  # Type=FIFO, add .fifo to name
        logger.info(f'Created SNS topic {name}.')

    except ClientError:
        logger.exception(f'Could not create SNS topic {name}.')
        raise
    else:
        return topic

def list_topics():
    """
    Lists all SNS notification topics using paginator.
    """
    try:

        paginator = client.get_paginator('list_topics')

        # creating a PageIterator from the paginator
        page_iterator = paginator.paginate().build_full_result()

        topics_list = []

        # loop through each page from page_iterator
        for page in page_iterator['Topics']:
            topics_list.append(page['TopicArn'])
    except ClientError:
        logger.exception(f'Could not list SNS topics.')
        raise
    else:
        return topics_list

def list_topic_attributes():
    """
    Lists all SNS topics attributes using paginator.
    """
    try:

        paginator = client.get_paginator('list_topics')

        # creating a PageIterator from the paginator
        page_iterator = paginator.paginate().build_full_result()

        topic_attributes_list = []

        # loop through each page from page_iterator
        for page in page_iterator['Topics']:
            
            response = client.get_topic_attributes(
                TopicArn=page['TopicArn']
            )['Attributes']
            
            dict_obj = {
                'TopicArn': page['TopicArn'],
                'TopicPolicy': json.loads(response['Policy'])
            }
            
            topic_attributes_list.append(dict_obj)
            
    except ClientError:
        logger.exception(f'Could not get SNS topic attributes.')
        raise
    else:
        return topic_attributes_list


def publish_message(topic_arn, message, subject):
    """
    Publishes a message to a topic.
    """
    try:

        response = client.publish(
            TopicArn=topic_arn,
            Message=message,
            Subject=subject,
        )['MessageId']

    except ClientError:
        logger.exception(f'Could not publish message to the topic.')
        raise
    else:
        return response


def main():
    topic_name = 'hands-on-cloud-sns-topic'
    logger.info(f'Creating SNS topic {topic_name}...')
    topic = create_topic(topic_name)

    logger.info(f'Listing all SNS topics...')
    topics = list_topics()

    for topic in topics:
        logger.info(topic)


    topic_arn = 'arn:aws:sns:us-east-2:000000000000:hands-on-cloud-sns-topic'
    message = 'create team blue-team'
    subject = 'This is a message subject on topic.'

    logger.info(f'Publishing message to topic - {topic_arn}...')
    message_id = publish_message(topic_arn, message, subject)
    logger.info(
        f'Message published to topic - {topic_arn} with message Id - {message_id}.'
    )

if __name__ == "__main__":
    main()




