import sys
import os

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", None)
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", None)
AWS_REGION = os.getenv("AWS_REGION", None)
COGNITO_USER_POOL_ID = os.getenv("COGNITO_USER_POOL_ID", None)
COGNITO_APP_CLIENT_ID = os.getenv("COGNITO_APP_CLIENT_ID", None)

HOST_NAME = os.getenv("HOST_NAME", "localhost")
HOST_PORT = os.getenv("HOST_PORT", "8000")
HOST_PROTOCOL = os.getenv("HOST_PROTOCOL", "http")

TABLE_NAME = "users"

if AWS_ACCESS_KEY_ID is None:
    print("Please set AWS_ACCESS_KEY_ID !!!")
    sys.exit(1)
elif AWS_SECRET_ACCESS_KEY is None:
    print("Please set AWS_SECRET_ACCESS_KEY !!!")
    sys.exit(1)
elif AWS_REGION is None:
    print("Please set AWS_REGION !!!")
    sys.exit(1)
elif COGNITO_USER_POOL_ID is None:
    print("Please set COGNITO_USER_POOL_ID !!!")
    sys.exit(1)
elif COGNITO_APP_CLIENT_ID is None:
    print("Please set COGNITO_APP_CLIENT_ID !!!")
    sys.exit(1)
