import boto3
import logging
import uuid
import utils.constants as constant

from boto3.dynamodb.conditions import Key
from flask import request
from users import settings
from datetime import datetime
from flask_cors import cross_origin
from utils.utils import (
    GetResponseObject,
    CreateErrorObject)

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


def put_accountNumber(accountNumber):
    dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)

    table = dynamodb.Table('recurringPayments')
    response = table.put_item(
       Item={
            'accountNumber': accountNumber,
            'recurringTransactions': [],
        }
    )
    return response


@cross_origin()
def create_internal_transaction():
    if request and request.method != "POST":
        data = f"Invalid request method, method {request.method} not supported !!!"
        res = GetResponseObject(data, 405)
        log.error(res)
        return res

    if not request.data:
        data = f"Empty request body !!!!"
        res = GetResponseObject(data, 400)
        return res

    dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)

    transactionID = str(uuid.uuid1())

    amount = request.json.get('amount')
    if amount is None:
        res = CreateErrorObject(404, constant.STATUS_BAD_REQUEST, "Amount Not Specified", "Amount not provided.",
                                "Enter the value for amount")
        return res
    if amount == 0:
        res = CreateErrorObject(404, constant.STATUS_BAD_REQUEST, "Invalid amount entered", "Amount cannot be 0",
                                "Enter an amount greater than 0")
        return res
    if amount < 0:
        res = CreateErrorObject(404, constant.STATUS_BAD_REQUEST, "Invalid amount entered", "Amount cannot be negative",
                                "Enter an amount greater than 0")
        return res

    transactionType = request.json.get('transactionType')
    description = request.json.get('description')
    if description is None:
        if transactionType == "debit":
            description = 'The amount {} is withdrawn'.format(amount)
        else:
            description = 'The amount {} is deposited'.format(amount)

    fromAcc = request.json.get('fromAcc')
    toAcc = request.json.get('toAcc')

    if toAcc is None:
        Acc = fromAcc
    else:
        Acc = toAcc

    modeOfTransaction = request.json.get('modeOfTransaction')
    if modeOfTransaction is None:
        modeOfTransaction = "online"

    table = dynamodb.Table('transactions')
    # Calculate account balance
    response = table.query(KeyConditionExpression=Key('accountNumber').eq(str(Acc)))
    items = response['Items']
    if len(items) > 0:
        accountBalance = items[0]['accountBalance']
        if transactionType == "debit":
            accountBalance = accountBalance - amount
            if int(accountBalance) < 0:
                res = CreateErrorObject(404, constant.STATUS_BAD_REQUEST, "Insufficient funds available to make this transaction",
                                        "Not enough account balance to make this transaction",
                                        "Either add money to your account or make a transaction of lesser amount")
                return res

        elif transactionType == "credit":
            accountBalance = accountBalance + amount
        else:
            res = CreateErrorObject(404, constant.STATUS_BAD_REQUEST, "Invalid transaction type",
                                    "transaction type can be either credit or debit",
                                    "Transaction type can be either credit/debit")
            return res

    now = datetime.now()
    timestamp = str(now)

    transaction = {'transactionID': transactionID, 'amount': amount, 'accountBalance': accountBalance, 'description': description,
                   'fromAcc': str(fromAcc), 'toAcc': str(toAcc), 'modeOfTransaction': modeOfTransaction,
                   'transactionType': transactionType, 'dateTime': timestamp}

    transactionResponse = table.update_item(
            Key={
                'accountNumber': str(Acc),
            },
            UpdateExpression="set accountBalance = :ab, transactions = list_append(transactions, :tr)",
            ExpressionAttributeValues={
                ':ab': accountBalance,
                ':tr': [transaction],
            },
            ReturnValues="UPDATED_NEW"
    )

    if transactionResponse["ResponseMetadata"]["HTTPStatusCode"] == 200:
        data = {
            "success": "true",
            "Message": "Transaction successful"
        }
        return data
    else:
        errData = {
            "success": "false",
            "Message": "Transaction failed"
        }
        return errData

@cross_origin()
def create_external_transaction():
    if request and request.method != "POST":
        data = f"Invalid request method, method {request.method} not supported !!!"
        res = GetResponseObject(data, 405)
        log.error(res)
        return res

    if not request.data:
        data = f"Empty request body !!!!"
        res = GetResponseObject(data, 400)
        return res

    dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)

    transactionID1 = uuid.uuid1()
    transactionID2 = uuid.uuid1()

    amount = request.json.get('amount')
    if amount is None:
        res = CreateErrorObject(404, constant.STATUS_BAD_REQUEST, "Amount Not Specified", "Amount not provided.", "Enter the value for amount")
        return res
    if amount == 0:
        res = CreateErrorObject(404, constant.STATUS_BAD_REQUEST, "Invalid amount entered", "Amount cannot be 0", "Enter an amount greater than 0")
        return res
    if amount < 0:
        res = CreateErrorObject(404, constant.STATUS_BAD_REQUEST, "Invalid amount entered", "Amount cannot be negative", "Enter an amount greater than 0")
        return res

    fromAcc = request.json.get('fromAcc')
    toAcc = request.json.get('toAcc')

    fromTransactionType = "debit"
    toTransactionType = "credit"

    fromTransactionDescription = request.json.get('description')
    if fromTransactionDescription is None:
        fromTransactionDescription = 'The amount {} is sent to account number {}'.format(amount, toAcc)

    toTransactionDescription = 'The amount {} is deposited from account number {}'.format(amount, fromAcc)

    modeOfTransaction = request.json.get('modeOfTransaction')
    if modeOfTransaction is None:
        modeOfTransaction = "online"

    table = dynamodb.Table('transactions')
    # Calculate available balance
    fromAccResponse = table.query(KeyConditionExpression=Key('accountNumber').eq(str(fromAcc)))
    fromAccItems = fromAccResponse['Items']
    if len(fromAccItems) > 0:
        accountBalance = fromAccItems[0]['accountBalance']
        fromAccountBalance = accountBalance - amount
        if int(fromAccountBalance) < 0:
            res = CreateErrorObject(404, constant.STATUS_BAD_REQUEST,
                                    "Insufficient funds available to make this transaction",
                                    "Not enough account balance to make this transaction",
                                    "Either add money to your account or make a transaction of lesser amount")
            return res

    toAccResponse = table.query(KeyConditionExpression=Key('accountNumber').eq(str(toAcc)))
    toAccItems = toAccResponse['Items']
    if len(toAccItems) > 0:
        accountBalance = toAccItems[0]['accountBalance']
        toAccountBalance = accountBalance + amount

    now = datetime.now()
    timestamp = str(now)

    fromtransaction = {'M': {'transactionID': {'S': str(transactionID1)}, 'amount': {'N': str(amount)}, 'accountBalance': {'N': str(fromAccountBalance)},
                             'description': {'S': str(fromTransactionDescription)},
                             'fromAcc': {'S': str(fromAcc)}, 'toAcc': {'S': str(toAcc)},
                             'modeOfTransaction': {'S': str(modeOfTransaction)},
                             'transactionType': {'S': str(fromTransactionType)}, 'dateTime': {'S': str(timestamp)}}}

    totransaction = {'M': {'transactionID': {'S': str(transactionID2)}, 'amount': {'N': str(amount)}, 'accountBalance': {'N': str(toAccountBalance)},
                           'description': {'S': str(toTransactionDescription)},
                           'fromAcc': {'S': str(fromAcc)}, 'toAcc': {'S': str(toAcc)},
                           'modeOfTransaction': {'S': str(modeOfTransaction)},
                           'transactionType': {'S': str(toTransactionType)}, 'dateTime': {'S': str(timestamp)}}}

    transactionResponse = client.transact_write_items(
        TransactItems=[
            {
                'Update': {
                    'Key': {
                        'accountNumber': {'S': str(toAcc)},
                    },
                    'UpdateExpression': 'set accountBalance = :ab, transactions = list_append(transactions, :tr)',
                    'TableName': 'transactions',
                    'ExpressionAttributeValues': {
                        ':ab': {'N': str(toAccountBalance)},
                        ':tr': {'L': [totransaction]},
                    },
                    'ReturnValuesOnConditionCheckFailure': 'NONE',
                },
            },
            {
                'Update': {
                    'Key': {
                        'accountNumber': {'S': str(fromAcc)},
                    },
                    'UpdateExpression': 'set accountBalance = :accbal, transactions = list_append(transactions, :transact)',
                    'TableName': 'transactions',
                    'ExpressionAttributeValues': {
                        ':accbal': {'N': str(fromAccountBalance)},
                        ':transact': {'L': [fromtransaction]},
                    },
                    'ReturnValuesOnConditionCheckFailure': 'NONE',
                }
            },
        ]
    )

    if transactionResponse["ResponseMetadata"]["HTTPStatusCode"] == 200:
        data = {
            "success": "true",
            "Message": "Transaction successful"
        }
        return data
    else:
        errData = {
            "success": "false",
            "Message": "Transaction failed"
        }
        return errData

@cross_origin()
def create_recurring_transaction():
    if request and request.method != "POST":
        data = f"Invalid request method, method {request.method} not supported !!!"
        res = GetResponseObject(data, 405)
        log.error(res)
        return res

    if not request.data:
        data = f"Empty request body !!!!"
        res = GetResponseObject(data, 400)
        return res

    dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)

    amount = request.json.get('amount')
    if amount is None:
        res = CreateErrorObject(404, constant.STATUS_BAD_REQUEST, "Amount Not Specified", "Amount not provided.", "Enter the value for amount")
        return res
    if amount == 0:
        res = CreateErrorObject(404, constant.STATUS_BAD_REQUEST, "Invalid amount entered", "Amount cannot be 0", "Enter an amount greater than 0")
        return res
    if amount < 0:
        res = CreateErrorObject(404, constant.STATUS_BAD_REQUEST, "Invalid amount entered", "Amount cannot be negative", "Enter an amount greater than 0")
        return res

    fromAcc = request.json.get('fromAcc')
    toAcc = request.json.get('toAcc')

    # get the number of months
    numberOfMonths = request.json.get('numberOfMonths')
    if numberOfMonths < 1:
        res = CreateErrorObject(404, constant.STATUS_BAD_REQUEST, "Invalid number of months entered", "Number of months cannot be lesser than 1",
                                "Enter a value greater than or equal to 1")
        return res

    now = datetime.now()
    timestamp = str(now)

    table = dynamodb.Table('recurringPayments')

    toAccResponse = table.query(KeyConditionExpression=Key('accountNumber').eq(str(fromAcc)))
    toAccItems = toAccResponse['Items']
    if len(toAccItems) == 0:
        # create a an item put operation
        put_accountNumber(str(fromAcc))

    recurringTransaction = {'amount': amount, 'toAcc': toAcc, 'nextTransactionDate': timestamp,
                           'noOfMonthsPending': numberOfMonths}

    recurringTransactionResponse = table.update_item(
        Key={
            'accountNumber': str(fromAcc),
        },
        UpdateExpression="set recurringTransactions = list_append(recurringTransactions, :rt)",
        ExpressionAttributeValues={
            ':rt': [recurringTransaction],
        },
        ReturnValues="UPDATED_NEW"
    )

    if recurringTransactionResponse["ResponseMetadata"]["HTTPStatusCode"] == 200:
        data = {
            "success": "true",
            "Message": "Transaction successful"
        }
        return data
    else:
        errData = {
            "success": "false",
            "Message": "Transaction failed"
        }
        return errData
