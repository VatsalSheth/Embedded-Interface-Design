"""*******************************************************************************************************
 * File Name: lambda.py
 * Description: This code implements AWS Lambda function which calls AWS SNS and AWS SQS services.
 * Date: 10/23/2019
 * 
 * ****************************************************************************************************"""

import json
import boto3

#AWS Lambda handler function 
def lambda_handler(event, context):
    # TODO implement
    print(json.dumps(event))
   
    if event["id"] == "D":
        sqs = boto3.resource('sqs')
        queue = sqs.get_queue_by_name(QueueName='dht')
        response = queue.send_message(MessageBody=json.dumps(event))
    elif event["id"] == "A":
        msg = event["S"];
        sns = boto3.client('sns')
        response = sns.publish (
            TopicArn = 'arn:aws:sns:us-east-1:294858239602:sns_test',
            Message = msg
        )
       
    
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
