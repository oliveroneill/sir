"""
Handler for checking the invitation code and displaying the RSVP form.

This module contains some useful util functions for displaying error
messages and checking whether an invite code is valid.
"""
import os

import dynamodb
import jinja2
import requests


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

    spotify_api_token = get_spotify_api_token()
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "text/html"},
        # The invite information is used to render the form
        "body": template.render(**invitee, spotify_api_token=spotify_api_token)
    }


def get_spotify_api_token():
    """
    Make request to create a Spotify access token.

    This will check an environment variable named "SPOTIFY_CLIENT_SECRET",
    which should be set to a base64 encoding of client_id:client_secret

    See https://developer.spotify.com/documentation/general/guides/authorization-guide/#client-credentials-flow
    for details.
    """
    spotify_api_token = os.environ.get("SPOTIFY_CLIENT_SECRET")
    if spotify_api_token is None:
        return None
    headers = {"Authorization": "Basic " + spotify_api_token}
    data = {'grant_type': 'client_credentials'}
    r = requests.post(
        'https://accounts.spotify.com/api/token',
        data=data, headers=headers
    )
    response = r.json()
    return response.get("access_token")


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
