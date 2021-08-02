import json
import requests
import base64
from flask import Response, jsonify, request
from users import settings
from jose import jwt, jwk
from jose.utils import base64url_decode


# utility class to get username, id and to check if token is expired
class JWTTokenUtil:
    def __init__(self, token):
        self.token = token
        self.decoded_token = jwt.get_unverified_claims(token)

    def get_user(self):
        if self.decoded_token and 'username' in self.decoded_token:
            return self.decoded_token['username']

    def get_user_id(self):
        if self.decoded_token and 'sub' in self.decoded_token:
            return self.decoded_token['sub']

    def is_token_expired(self):
        import datetime
        now = datetime.datetime.now()
        if self.decoded_token:
            if now > datetime.datetime.fromtimestamp(self.decoded_token['exp']):
                return True

            return False


def verify_token(view_func):
    from functools import wraps
    @wraps(view_func)
    def is_token_expired(token):
        import datetime
        now = datetime.datetime.now()
        dec_access_token = jwt.get_unverified_claims(token)

        if now > datetime.datetime.fromtimestamp(dec_access_token['exp']):
            return True, 'Access Token has expired'

        return False, 'Valid Access Token'

    def check_token(token):
        # Decode token header
        token_header = jwt.get_unverified_header(token)
        # Decode token payload
        jwt.get_unverified_claims(token)

        jwks_url = f"https://cognito-idp.{settings.AWS_REGION}.amazonaws.com/{settings.COGNITO_USER_POOL_ID}/.well-known/jwks.json"

        r = requests.get(jwks_url)
        if r.status_code == 200:
            jwks = r.json()
        else:
            return False, f"Did not retrieve JWKS, got {r.status_code}"

        kid = token_header['kid']
        # Search the JWKS for the proper public key
        key_index = -1
        for i in range(len(jwks['keys'])):
            if kid == jwks['keys'][i]['kid']:
                key_index = i
                break
        if key_index == -1:
            return False, "Public key not found, can not verify token"
        else:
            # Convert public key
            public_key = jwk.construct(jwks['keys'][key_index])
            # Get claims and signature from token
            claims, encoded_signature = token.rsplit('.', 1)
            # Verify signature
            decoded_signature = base64url_decode(
                encoded_signature.encode('utf-8'))

            if not public_key.verify(claims.encode("utf8"),
                                     decoded_signature):
                return False, "Signature verification failed"
            else:
                return True, "Signature successfully verified"

    def helper(*args, **kwargs):
        token_prefix = "Bearer"

        try:
            auth = request.headers.get('authorization', b'').split()
            if not auth or auth[0].lower() != token_prefix.lower():
                return jsonify("Invalid credentials/token !!!"), 403

            if len(auth) == 1:
                msg = 'Invalid token header. No credentials provided.'
                return jsonify(msg), 403

            elif len(auth) > 2:
                msg = 'Invalid token header. Token string should not contain spaces.'
                return jsonify(msg), 403

            resp, err = is_token_expired(auth[1])
            if resp:
                return jsonify({"msg": str(err)}), 403

            resp, err = check_token(auth[1])
            if not resp:
                return jsonify({"msg": str(err)}), 403

            return view_func(*args, **kwargs)

        except Exception as e:
            return jsonify({"msg": str(e)}), 403

    return helper


def GetResponseObject(data, status=500, success=False):
    data = {
        "status": status,
        "success": success,
        "data": data
    }

    response = Response(json.dumps(data), status=status)
    response.mimetype = "application/json"
    return response


def GetUserPasswordFromAuthHeader(request):
    auth_prefix = "Basic"

    auth_header = request.headers.get('AUTHORIZATION', b'')
    encoded_credentials = auth_header.split()

    if (not encoded_credentials) or (encoded_credentials[0].lower() != auth_prefix.lower()):
        return None, "Get user credentials from auth header failed !!!"

    if len(encoded_credentials) == 1:
        return None, "Invalid authorization header. NO credentials provided !!!"

    if len(encoded_credentials) > 2:
        return None, "Invalid token header !!!"

    decoded_credentials = base64.b64decode(encoded_credentials[1]).decode("utf-8").split(":")

    return decoded_credentials, None


def GetTokenFromHeader(request, token_name, token_prefix, sep=":"):
    try:
        auth = request.headers.get(token_name.upper(), b'').split(sep)
        if not auth or auth[0].lower() != token_prefix.lower():
            return None, 'Invalid credentials/token !!!'

        if len(auth) == 1:
            msg = 'Invalid token header. No credentials provided.'
            return None, msg

        elif len(auth) > 2:
            msg = 'Invalid token header. Token string should not contain spaces.'
            return None, msg

        return auth[1], None
    except Exception as e:
        return None, str(e)

def CreateErrorObject(errorCode, errorStatusCode, message, details, recommendedActions):
    error = {
        "errorCode": errorCode,
        "errorStatusCode": errorStatusCode,
        "message": message,
        "details": details,
        "recommendedActions": recommendedActions
    }

    response = Response(json.dumps(error), status="error")
    response.mimetype = "application/json"
    return response
