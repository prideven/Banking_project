from datetime import datetime
from random import randint
import boto3
import logging
from boto3 import resource
from boto3.dynamodb.conditions import Key,Attr
from botocore.exceptions import ClientError
from datetime import date
from dateutil.relativedelta import relativedelta
import utils.constants as constant
from users import settings
from flask_cors import cross_origin
from flask import request, jsonify  # import flask
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


@cross_origin()
def getAccount(userName):
    if userName:
        dynamodb = resource('dynamodb', region_name=AWS_REGION)
        table = dynamodb.Table("transactions")
        scan_kwargs = {
        'FilterExpression': Key('userName').eq(userName)}
        getAccount_response = table.scan(**scan_kwargs)
        res = []
        if getAccount_response["ResponseMetadata"]["HTTPStatusCode"] == 200:
            items = getAccount_response['Items']
            if len(items) > 0:
                for i, item in enumerate(items):
                    res.append({
                                'accountNumber': item['accountNumber'],
                                'accountType' : item['accountType'],
                                'accountBalance' : str(item['accountBalance'])
                            })
            
            data = {
                "success": "true",
                "data": res
            }
            return jsonify(data)
        else:
            errData = {
                "success": "false",
                "Message": "DB operation Failed, try again!"
            }
            return errData


@cross_origin()
def createAccount(userName):
    if request and request.method != "POST":
        data = f"Invalid request method, method {request.method} not supported !!!"
        res = GetResponseObject(data, 405)
        log.error(res)
        return res

    if not request.data:
        data = f"Empty request body !!!!"
        res = GetResponseObject(data, 400)
        return res

    accountType = request.json.get('account_type')
    accountBalance = 0

    if accountType is None:
        res = CreateErrorObject(404, constant.STATUS_BAD_REQUEST, "AccountType Not entered", "Account Type is not added.",
                                "Enter an account type")
        return res
    #to generate account number
    now=datetime.now()
    timestamp=str(int(datetime.timestamp(now)))
    random_num=str(randint(100, 999))
    accountNumber=random_num+timestamp

    if userName:
        dynamodb = resource('dynamodb', region_name=AWS_REGION)
        table = dynamodb.Table("transactions")
    else:
        return"No username found"
    try:
        create_account_response= table.put_item(
           Item={
               'accountNumber' : accountNumber,
               'userName':userName,
               'accountBalance':accountBalance,
               'accountType':accountType,
               'transactions': []
                }
        )
    except ClientError as e:
        errData = {
            "success": "false",
            "Message": "DB operation Failed,try again!"
        }
        return errData

    if create_account_response ["ResponseMetadata"]["HTTPStatusCode"] == 200:
        message = {
            "success": "true",
            "Message": "Successfully created account"
        }
    return jsonify(message)


@cross_origin()
def deleteAccount(userName,accountNumber):
    dynamodb = resource('dynamodb', region_name=AWS_REGION)
    table = dynamodb.Table("transactions")
    try:
        delete_account_response = table.delete_item(
            Key={
                'accountNumber': accountNumber
            },
        ConditionExpression='attribute_exists(accountNumber)'
        )
    except ClientError as e:
        res = CreateErrorObject(404, constant.STATUS_BAD_REQUEST, "Invalid Account Number", "Invalid Account Number",
                                "Enter a valid account number")
        return res
    if delete_account_response["ResponseMetadata"]["HTTPStatusCode"] == 200:
        message = {
            "success": "true",
            "Message": "Account is deleted successfully"
        }
    return jsonify(message)


@cross_origin()
def getTransactions(userName,accountNumber):
    dynamodb = resource('dynamodb', region_name=AWS_REGION)
    table = dynamodb.Table("transactions")
    get_transaction_response= table.query(KeyConditionExpression=Key('accountNumber').eq(accountNumber))
    items= get_transaction_response['Items']
    start_date = date.today() + relativedelta(months=-18)
    end_date=date.today()
    if len(items)>0:
        try:
            transaction=items[0]['transactions']
        except:
            data = {
                "success": "true",
                "data": [{'transactions':[],'accountType':items[0]['accountType'],'accountBalance': str(items[0]['accountBalance'])}]
            }
            return jsonify(data)
        transaction_store=[]
        for valid_transaction in transaction:
            if valid_transaction['dateTime']:
                db_date=valid_transaction['dateTime'][:10]
                db_date=datetime.strptime(db_date, '%Y-%m-%d').date()
                try:
                    transactionID = valid_transaction['transactionID']
                except:
                    transactionID = ""
                if start_date <= db_date <= end_date:
                    transaction_store.append({
                        'accountBalance':str(valid_transaction['accountBalance']),
                        'amount':str(valid_transaction['amount']),
                        'dateTime':valid_transaction['dateTime'],
                        'description':valid_transaction['description'],
                        'fromAcc':valid_transaction['fromAcc'],
                        'modeOfTransaction':valid_transaction['modeOfTransaction'],
                        'toAcc':valid_transaction['toAcc'],
                        'transactionType':valid_transaction['transactionType'],
                        'transactionID': transactionID,
                    })

    if get_transaction_response["ResponseMetadata"]["HTTPStatusCode"] == 200 and len(items)>0:

        data = {
            "success": "true",
            "data":[{'transactions':(transaction_store),'accountType':items[0]['accountType'],'accountBalance': str(items[0]['accountBalance'])}]
        }
        return jsonify(data)
    else:
        res = CreateErrorObject(404, constant.STATUS_BAD_REQUEST, "Invalid Account Number", "Invalid Account Number",
                                "Provide a valid account number")
        return res
