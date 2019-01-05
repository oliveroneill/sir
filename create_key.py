"""A script to generate a db record and code for a specified invitee."""
import argparse
import random
import string

import boto3
from boto3.dynamodb.conditions import Key

# Default settings for invitation form
DEFAULT_VALUES = {
    'food': None,
    'going': True,
    'plus_one': False,
    'plus_one_name': None,
    'plus_one_food': None,
    'music': None,
    'notes': None,
    'song_id': None,
    # sent_rsvp is used to identify guests that haven't RSVP'd yet
    'sent_rsvp': False,
}


def generate_code():
    """Generate a 5 character string made of upper case letters and digits."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))


def generate_unique_code(table):
    """
    Generate a unique code by ensuring that the code doesn't exist in the db.

    This will keep recreating codes until it finds one that isn't in the
    database.

    Args:
        table: A DynamoDB table for quering the code

    Returns:
        A 5 character code that isn't currently in the specified table.
    """
    code = generate_code()
    # Loop until we find a code that isn't used
    while not is_code_unique(table, code):
        code = generate_code()
    return code


def is_code_unique(table, code):
    """
    Check whether the code already exists in the table.

    Args:
        table: A DynamoDB table for quering the code
        code: A generated code
    """
    response = table.query(
        KeyConditionExpression=Key('invite_code').eq(code)
    )
    return len(response['Items']) == 0


def create_key(name):
    """
    Add this invitee to the database by using the specified name.

    This will fill the record with default values.

    Args:
        name: The name of the invitee.
    """
    dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('Invitations')

    code = generate_unique_code(table)
    record = {
        'name': name,
        'invite_code': code
    }
    # Add the default values
    record.update(DEFAULT_VALUES)
    table.put_item(Item=record)
    print("Successfully added invitee. Invitation code is", code)
    return code


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Create DynamoDB records for invitees.'
    )
    parser.add_argument('name', type=str, help='Invitee name')
    args = parser.parse_args()

    create_key(name=args.name)
