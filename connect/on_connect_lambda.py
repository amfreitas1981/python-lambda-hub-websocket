import json
import boto3
import os
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamo_db = boto3.client('dynamodb')
TABLE_NAME = os.environ.get("TABLE_NAME")

def lambda_handler(event, context):
    logger.info("Connection event: %s", json.dumps(event))

    try:
        connection_id = event["requestContext"]["connectionId"]
        session_id = (event.get("queryStringParameters") or {}).get("session")

        if not session_id:
            logger.warning("Missing 'session' query parameter.")
            return {
                'statusCode': 400, 'body': "Missing session parameter"
            }

        # Grava um único item com connection_id como chave primária
        dynamo_db.put_item(
            TableName=TABLE_NAME,
            Item={
                'connection_id': {'S': connection_id},
                'session_id': {'S': session_id}
            }
        )

        logger.info("Stored connection_id %s with session_id %s", connection_id, session_id)
        return {
            'statusCode': 200
        }

    except Exception as e:
        logger.exception("Error during connect event")
        return {
            'statusCode': 500, 'body': str(e)
        }
