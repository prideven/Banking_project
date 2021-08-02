import boto3
import json
import logging
from flask import request
from flask_cors import cross_origin
from users import settings

from warrant import Cognito

from botocore.exceptions import ClientError

from users.schema import ValidateRegistrationData

from utils.utils import (
    GetUserPasswordFromAuthHeader, GetResponseObject, \
    verify_token)

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
client = boto3.client("cognito-idp", \
                      aws_access_key_id=AWS_ACCESS_KEY_ID, \
                      aws_secret_access_key=AWS_SECRET_ACCESS_KEY, \
                      region_name=AWS_REGION)




def sign_in():
    if request and request.method != "GET":
        data = f"Invalid request method, method {request.method} not supported !!!"
        return GetResponseObject(data, 405)

    resp, err = GetUserPasswordFromAuthHeader(request)
    if err:
        log.error(err)
        res = GetResponseObject(err, 400)
        return res

    username, password = resp[0], resp[1]

    try:
        user = Cognito(user_pool_id=COGNITO_USER_POOL_ID, \
            client_id=COGNITO_APP_CLIENT_ID, \
            user_pool_region=AWS_REGION, \
            username=username)

        user.admin_authenticate(password=password)
        user_rec = user.admin_get_user()

        profile = {}

        for k,v in user_rec._data.items():
            if k == "given_name":
                profile["firstName"] = v
            elif k == "family_name":
                profile["lastName"] = v
            elif k == "email":
                profile["email"] = v
            elif k == "phone_number":
                profile["phoneNumber"] = v
            elif k == "custom:isAdmin":
                profile["isAdmin"] = v

        data = {
            "profile": profile,
            "idToken": user.id_token,
            "accessToken": user.access_token,
            "refreshToken": user.refresh_token,
        }
        res = GetResponseObject(data, 200, True)
        res.headers['HMS-TOKEN'] = "Bearer " + user.access_token
        return res

    except Exception as e:
        msg = f"Error while authenticating user {str(e)}"
        return GetResponseObject(msg)
        # return HttpResponseServerError(res)


def sign_up():
    try:
        if request and request.method != "POST":
            data = f"Invalid request method, method {request.method} not supported !!!"
            res = GetResponseObject(data, 405)
            log.error(res)
            return res

        resp, err = GetUserPasswordFromAuthHeader(request)
        if err:
            res = GetResponseObject(err, 401)
            log.error(res)
            return res

        username, password = resp[0], resp[1]

        if not request.data:
            data = f"Empty request body !!!!"
            res = GetResponseObject(data, 400)
            log.error(err)
            return res


        body = json.loads(request.data)
        resp, err = ValidateRegistrationData(body)
        if err:
            res = GetResponseObject(err, 400)
            log.error(res)
            return res

        body["userName"] = username
        # Save user record in Cognito
        user = Cognito(user_pool_id=COGNITO_USER_POOL_ID, client_id=COGNITO_APP_CLIENT_ID, user_pool_region=AWS_REGION)
        user.add_base_attributes(
            email=body["email"],
            given_name=body["firstName"],
            family_name=body["lastName"],
            phone_number=body["phoneNumber"]
        )

        if "isAdmin" in body:
            if body["isAdmin"] not in ["true", "false"]:
                return GetResponseObject("Invalid value for isAdmin (e.g. true/false), required bool", 400)

            user.add_custom_attributes(
                isAdmin=body["isAdmin"]
            )

        resp = user.register(username, password)

        user.admin_confirm_sign_up()
        body["uuid"] = resp['UserSub']

        data = "User registered successfully !!!"
        res = GetResponseObject(data, 200, True)
        return res

    except ClientError as e:
        if e.response['Error']['Code'] == 'UsernameExistsException':
            data = f"{username} username already exists !!!"
            log.error(data)
            res = GetResponseObject(data)
            return res

        data = f"Error: {str(e)}"
        log.error(data)
        res = GetResponseObject(data)
        return res
    
    except json.decoder.JSONDecodeError as e:
        return GetResponseObject(str(e), 400)


    except Exception as e:
        user = Cognito( \
            user_pool_id=COGNITO_USER_POOL_ID, \
            client_id=COGNITO_APP_CLIENT_ID, \
            user_pool_region=AWS_REGION,
            username=username)

        user.authenticate(password=password)
        resp = client.delete_user(AccessToken=user.access_token)

        log.info(f"Deleting user due to error while signing up: {resp}")
        data = f"Error while registering user: {str(e)}"
        log.error(data)
        res = GetResponseObject(data)
        return res


@cross_origin()
@verify_token
def sign_out():
    if request and request.method != "GET":
        data = f"Invalid request method, method {request.method} not supported !!!"
        res = GetResponseObject(data, 405)
        return res

    try:
        auth = request.headers.get('AUTHORIZATION', b'').split()
        response = client.global_sign_out(AccessToken=auth[1])
        data = "User signed out successfully !!!"
        res = GetResponseObject(data, 200, True)
        return res
    except Exception as e:
        msg = f"Error while signing out user: {str(e)}"
        log.error(msg)
        res = GetResponseObject(msg)
        return res


@cross_origin()
@verify_token
def delete_user():
    if request and request.method != "DELETE":
        data = f"Invalid request method, method {request.method} not supported !!!"
        res = GetResponseObject(data, 405)
        return res

    try:
        auth = request.headers.get('AUTHORIZATION', b'').split()

        # Delete user from cognito
        client.delete_user(AccessToken=auth[1])

        msg = "User deleted successfully !!!"
        res = GetResponseObject(msg, 200, True)
        return res

    except Exception as e:
        msg = f"Error while deleting user: {str(e)}"
        log.error(msg)
        res = GetResponseObject(msg)
        return res


@cross_origin()
@verify_token
def update_profile():
    if request and request.method != "PUT":
        data = f"Invalid request method, method {request.method} not supported !!!"
        return GetResponseObject(data, 405)

    try:
        auth = request.headers.get('AUTHORIZATION', b'').split()
        if not request.data:
            data = f"Empty request body !!!!"
            res = GetResponseObject(data, 400)
            log.error(err)
            return res

        body = json.loads(request.data)
        resp, err = ValidateRegistrationData(body, True)
        if err:
            res = GetResponseObject(err, 400)
            return res

        user = Cognito(
            user_pool_id=COGNITO_USER_POOL_ID,
            client_id=COGNITO_APP_CLIENT_ID,
            user_pool_region=AWS_REGION,
            access_token=auth[1]
        )

        profile = {}

        for k, v in body.items():
            if k == "firstName":
                profile["given_name"] = v
            elif k == "lastName":
                profile["family_name"] = v
            elif k == "email":
                profile["email"] = v
            elif k == "phoneNumber":

                profile["phone_number"] = v

        user.update_profile(profile, attr_map=dict())

        data = "User profile updated successfully !!!"
        res = GetResponseObject(data, 200, True)
        return res

    except Exception as e:
        data = f"Error while updating user profile: {str(e)}"
        log.error(data)
        res = GetResponseObject(data)
        return res
