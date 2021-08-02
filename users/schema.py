from jsonschema import validate, ValidationError, SchemaError

consumer_profile = {
    "$schema": "http://json-schema.org/draft-07/schema#",    
    "type": "object",
    "properties": {
        "firstName": {
            "type": "string"
        },
        "lastName": {
            "type": "string"
        },
        "phoneNumber": {
            "type": "string"
        },
        "email": {
            "type": "string"
        }
    },
    "required": ["firstName", "lastName", "phoneNumber", "email"]
}


update_consumer_profile = {
    "$schema": "http://json-schema.org/draft-07/schema#",    
    "type": "object",
    "properties": {
        "firstName": {
            "type": "string"
        },
        "lastName": {
            "type": "string"
        },
        "phoneNumber": {
            "type": "string"
        },
        "email": {
            "type": "string"
        }
    }
}


def ValidateRegistrationData(data, update=False):
    try:
        if not update:
            validate(data, consumer_profile)
        else:
            validate(data, update_consumer_profile)

        return True, None
    except SchemaError as e:
        return False, "Invalid user registration data" + str(e)
    except ValidationError as e:  
        return False, "User registration data validation error, " + str(e)