import boto3
import logging
import boto3
from boto3 import resource
from flask import jsonify
from flask_cors import cross_origin
from users import settings

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
log.propagate = True

AWS_ACCESS_KEY_ID = settings.AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY = settings.AWS_SECRET_ACCESS_KEY
AWS_REGION = settings.AWS_REGION
COGNITO_USER_POOL_ID = settings.COGNITO_USER_POOL_ID
COGNITO_APP_CLIENT_ID = settings.COGNITO_APP_CLIENT_ID

# creating aws cognito identity provider client
client = boto3.client("dynamodb",
                      aws_access_key_id=AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                      region_name=AWS_REGION)

@cross_origin()
def getFeesTrnsaction():
    dynamodb = resource('dynamodb', region_name=AWS_REGION)
    table = dynamodb.Table("transactions")
    getAccount_response = table.scan()
    transaction_store = []
    if getAccount_response["ResponseMetadata"]["HTTPStatusCode"] == 200:
        items = getAccount_response['Items']
        transaction_store = []
        if len(items) > 0:
            for i in range((len(items))):
                try:
                    transaction = items[i]['transactions']
                except:
                    continue

                for valid_transaction in transaction:
                    if valid_transaction['modeOfTransaction']=="fees":

                        try:
                            transactionID=valid_transaction['transactionID']
                        except:
                            transactionID=""

                        transaction_store.append({
                            'accountBalance': str(valid_transaction['accountBalance']),
                            'amount': str(valid_transaction['amount']),
                            'description': valid_transaction['description'],
                            'fromAcc': valid_transaction['fromAcc'],
                            'modeOfTransaction': valid_transaction['modeOfTransaction'],
                            'toAcc': valid_transaction['toAcc'],
                            'transactionType': valid_transaction['transactionType'],
                            'transactionID' : transactionID,
                            'dateTime': valid_transaction['dateTime']
                        })

        message = {
            "success": "true",
            "data": transaction_store
        }
        return jsonify(message)
    else:
        errData = {
            "success": "false",
            "Message": "DB operation Failed,try again!"
        }
