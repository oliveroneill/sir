"""Util functions for accessing data via DynamoDB."""
import boto3
from boto3.dynamodb.conditions import Key


class UnknownInviteCodeError(Exception):
    """An error when an unknown invite code is entered."""

    pass


def get_invitee(invite_code: str):
    """Get a dictionary of the stored information for this invite code."""
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Invitations')
    return get_invitee_from_table(invite_code, table)


def get_invitee_from_table(invite_code: str, table):
    """
    Get a dictionary of the stored information for this invite code.

    Args:
        invite_code: The invitation code to search for
        table: A DynamoDB table for querying

    Returns:
        A dictionary of information stored under the invite code

    Throws:
        UnknownInviteCodeError: If the invite code is not in the database
    """
    response = table.query(
        KeyConditionExpression=Key('invite_code').eq(invite_code)
    )

    items = response['Items']
    if len(items) == 0:
        # If there were no matches to the code then throw an error
        raise UnknownInviteCodeError()

    # The output will be a list, so we'll just use the first one since there
    # should not be duplicates
    items = items[0]

    # DynamoDB cannot store empty strings, so we use null instead and convert
    # between it as needed. At this point in time, we have no significance for
    # null so this works fine.
    items = {k: convert_null_to_empty_string(v) for k, v in items.items()}
    return items


def update_rsvp(data: dict):
    """
    Update the RSVP info for a invitee.

    The invite code will be retrieved from within the input dictionary.

    TODO: add data validation. This could possibly be done in API Gateway

    Args:
        data: A dictionary of data to be inserted into the database. The values
        here are expected to match the database schema.

    Throws:
        UnknownInviteCodeError: If the invite code is not in the database
    """
    code = data["invite_code"]
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Invitations')

    # Check that the code is known
    try:
        get_invitee_from_table(invite_code=code, table=table)
    except UnknownInviteCodeError:
        raise

    # Convert the data since DynamoDB can't handle empty strings
    data = {k: convert_empty_string_to_none(v) for k, v in data.items()}

    table.update_item(
        Key={
            'invite_code': code
        },
        UpdateExpression="set going = :g, food=:f, plus_one=:p, music=:m, notes=:n",
        ExpressionAttributeValues={
            ':g': data["going"],
            ':f': data["food"],
            ':p': data["plus_one"],
            ':m': data["music"],
            ':n': data["notes"]
        }
    )


def convert_null_to_empty_string(value):
    """
    Convert `None` type to empty strings.

    Used specifically to work around DynamoDB's limitation of not allowing
    empty strings.
    See https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Limits.html#limits-attributes

    Args:
        value: The value to convert to an empty string if None

    Returns:
        Empty string if value is None. If not, it will return the unchanged
        value
    """
    if value is None:
        return ""
    return value


def convert_empty_string_to_none(value):
    """
    Convert empty strings to `None` and leave others unchanged.

    Used specifically to work around DynamoDB's limitation of not allowing
    empty strings.
    See https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Limits.html#limits-attributes

    Empty strings will be entered into Dynamo as null values and converted
    using `convert_null_to_empty_string`

    Args:
        value: The value to convert to None if an empty string

    Returns:
        None if value is an empty string. Returns unchanged value otherwise
    """
    if isinstance(value, str) and len(value) == 0:
        return None
    return value
