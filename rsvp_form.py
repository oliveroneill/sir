"""
Handler for checking the invitation code and displaying the RSVP form.

This module contains some useful util functions for displaying error
messages and checking whether an invite code is valid.
"""
import os

import dynamodb
import jinja2


def rsvp_form(event, context):
    """
    Handle a request for an rsvp form.

    This page will follow on from the `enter_invite` page,
    it will either show an error message for an invalid key or it will display
    a form for the user to fill out to RSVP.

    The input will be of the form:
    http://example.com/rsvp_form?invite_code=E321
    where "E321" is the invite code to be checked and RSVP'd for.
    """
    # Retrieve code from query string
    code = event['queryStringParameters']['invite_code']
    # Get invite information
    try:
        invitee = dynamodb.get_invitee(invite_code=code)
    except dynamodb.UnknownInviteCodeError:
        # Show an error page if the code is unknown
        return error_page(code)

    template = jinja2.Environment(
        loader=jinja2.FileSystemLoader('./')
    ).get_template('public/tmpl/rsvp_form.html')

    spotify_api_token = os.environ.get("SPOTIFY_API_TOKEN")
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "text/html"},
        # The invite information is used to render the form
        "body": template.render(**invitee, spotify_api_token=spotify_api_token)
    }


def error_page(invite_code: str):
    """
    Get an error response page to return to Lambda.

    Args:
        invite_code: The invitation code to be displayed with the error message
    """
    template = jinja2.Environment(
        loader=jinja2.FileSystemLoader('./')
    ).get_template('public/tmpl/error.html')
    return {
        "statusCode": 403,
        "headers": {"Content-Type": "text/html"},
        "body": template.render(code=invite_code)
    }
