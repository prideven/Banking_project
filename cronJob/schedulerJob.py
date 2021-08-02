# This program calls create external transaction api for the time interval specified
import requests
import json
import boto3
from users import settings
from datetime import datetime
from dateutil.relativedelta import *

AWS_ACCESS_KEY_ID = settings.AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY = settings.AWS_SECRET_ACCESS_KEY
AWS_REGION = settings.AWS_REGION

url = "http://127.0.0.1:8000/externalTransact"

# creating aws cognito identity provider client
client = boto3.client("dynamodb",
                      aws_access_key_id=AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                      region_name=AWS_REGION)

# loop through the entire table
# take the account number, toAccountNumber, the amount, next payment date
# compare nextPayment date is equal to current date
# if yes perform the transaction
# if transaction is done update the next payment date
# update the months left

dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)
table = dynamodb.Table('recurringPayments')
response = table.scan()
items = response['Items']
length = len(items)
timestamp = datetime.now()
now = str(timestamp)
dateTimestamp = now[:10]

if length > 0:
    for i in range(length):
        fromAcc = items[i]['accountNumber']
        recurringTransactions = items[i]['recurringTransactions']
        for recurring_transaction in recurringTransactions:
            amount = recurring_transaction['amount']
            nextTransactionDate = recurring_transaction['nextTransactionDate'][:10]
            noOfMonthsPending = recurring_transaction['noOfMonthsPending']
            toAcc = recurring_transaction['toAcc']

            if dateTimestamp == nextTransactionDate and noOfMonthsPending > 0:
                payload = json.dumps({
                    "toAcc": str(toAcc),
                    "fromAcc": str(fromAcc),
                    "amount": str(amount),
                })
                print(payload)
                headers = {
                    'Content-Type': 'application/json'
                }

                response = requests.request("POST", url, headers=headers, data=payload)
                print(response)
                noOfMonthsPending = noOfMonthsPending - 1
                print(noOfMonthsPending)
                print(recurring_transaction['nextTransactionDate'])
                nextTransactionDate = recurring_transaction['nextTransactionDate'] + relativedelta(months=+1)
                print(nextTransactionDate)

                recurringTransaction = {
                    'nextTransactionDate': nextTransactionDate,
                    'noOfMonthsPending': noOfMonthsPending
                }

                recurringTransactionResponse = table.update_item(
                    Key={
                        'accountNumber': str(fromAcc),
                    },
                    UpdateExpression="set recurringTransactions[" + 1 + "].nextTransactionDate = :nt, recurringTransactions[" + 2 + "].noOfMonthsPending = :mp",
                    ExpressionAttributeValues={
                        ':nt': nextTransactionDate,
                        ':mp': noOfMonthsPending,
                    },
                    ReturnValues="UPDATED_NEW"
                )

                if recurringTransactionResponse["ResponseMetadata"]["HTTPStatusCode"] == 200:
                    data = {
                        "success": "true",
                        "Message": "Transaction successful"
                    }
                    print(data)
                else:
                    errData = {
                        "success": "false",
                        "Message": "Transaction failed"
                    }
                    print(errData)