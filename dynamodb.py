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


def get_invitee_from_table(invite_code: str, table: boto3.DynamoDB.Client):
    """
    Get a dictionary of the stored information for this invite code.

    Args:
        invite_code: The invitation code to search for
        table: A DynamoDB table for querying

    Returns:
        A dictionary of information stored under the invite code
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


def convert_null_to_empty_string(value):
    """
    Convert `None` type to empty strings.

    Used specifically to work around DynamoDB's limitation of not allowing
    empty strings.
    See https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Limits.html#limits-attributes

    TODO: consider moving this into a DAO.

    Args:
        value: The value to convert to an empty string if None

    Returns:
        Empty string if value is None. If not, it will return the unchanged
        value
    """
    if value is None:
        return ""
    return value
