import os
import sys
import logging

from users import settings
from pynamodb.models import Model
from pynamodb.connection import TableConnection
from pynamodb.attributes import (
    UnicodeAttribute
)

from pynamodb.indexes import GlobalSecondaryIndex, AllProjection

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
log.propagate = True


class NameIndex(GlobalSecondaryIndex):
    class Meta:
        index_name = "nameIdx"
        read_capacity_units = 1
        write_capacity_units = 1
        projection = AllProjection()

    name = UnicodeAttribute(hash_key=True)


class Users(Model):
    class Meta:
        read_capacity_units = 1
        write_capacity_units = 1
        table_name = settings.TABLE_NAME
        region = os.getenv("AWS_REGION")
        aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
        aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")

    uuid = UnicodeAttribute(hash_key=True)
    userName = UnicodeAttribute(null=False)
    email = UnicodeAttribute(null=False)
    firstName = UnicodeAttribute(null=False)
    lastName = UnicodeAttribute(null=False)
    phoneNumber = UnicodeAttribute(null=False)

    nameIndex = NameIndex()

    def save(self, **kwargs):
        return super(Users, self).save(**kwargs)


def InitUserTable():
    try:
        if not Users.exists():
            log.info("Creating Users table .....")
            Users.create_table(wait=True, read_capacity_units=1, write_capacity_units=1)
    except Exception as e:
        log.error(f"DB initialization failed: {str(e)}")
        sys.exit(1)


def SaveInDB(body, update=False):
    if body["userType"] == "provider":
        u = Users(
            userType=body["userType"],
            uuid=body["uuid"],
            username=body["username"],
            email=body["email"],
            firstName=body["firstName"],
            lastName=body["lastName"],
            phone=body["phone"],
            address=body["address"],
            area=body["area"],
            city=body["city"],
            days=body["days"],
            time=body["time"],
            skillSet=body["skillSet"],
            image="None",
            finalRating="0"
        )
    else:
        u = Users(
            userType=body["userType"],
            uuid=body["uuid"],
            username=body["username"],
            email=body["email"],
            firstName=body["firstName"],
            lastName=body["lastName"],
            phone=body["phone"],
            address=body["address"],
            area=body["area"],
            city=body["city"]
        )

    if update:
        u.update()
    else:
        u.save()


def UpdateItem(uid, userType, body=None, update=False, delete=False):
    try:
        conn = TableConnection(
            table_name=settings.TABLE_NAME,
            region=os.getenv("AWS_REGION"),
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
        )

        if delete:
            return conn.delete_item(hash_key=uid), None
        elif update and body:
            userObj = Users.get(uid)
            userObj.refresh()
            r = userObj.update(actions=[
                getattr(Users, k).set(v) for k, v in body.items()
            ])
            return r, None
    except Exception as e:
        return None, str(e)


def SerializeUserObj(user):
    if user.userType == "provider":
        out = {
            "userType": user.userType,
            "uuid": user.uuid,
            "username": user.username,
            "email": user.email,
            "firstName": user.firstName,
            "lastName": user.lastName,
            "phone": user.phone,
            "address": user.address,
            "area": user.area,
            "city": user.city,
            "image": user.image,
            "days": user.days,
            "time": user.time,
            "skillSet": [{"name": s.name, "price": s.price} for s in user.skillSet],
            "appointments": user.appointments,
            "finalRating": user.finalRating
        }
    else:
        out = {
            "userType": user.userType,
            "uuid": user.uuid,
            "username": user.username,
            "email": user.email,
            "firstName": user.firstName,
            "lastName": user.lastName,
            "phone": user.phone,
            "address": user.address,
            "area": user.area,
            "city": user.city,
            # "time": user.time,
            "appointments": user.appointments
        }

    return out
