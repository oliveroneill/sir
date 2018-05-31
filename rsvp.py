"""Handler for updating RSVP information."""
from urllib.parse import parse_qsl

import dynamodb
import jinja2
from rsvp_form import error_page


def rsvp(event, context):
    """
    Handle RSVP update event.

    Expects a request body in event, in the form of a query string.
    E.g: going=true&food=vegan&code=EF321

    This will return a success page or an error page, depending on whether the
    invite code is valid.
    """
    # Parse the query string into a dictionary
    body = dict(parse_qsl(event["body"]))
    # HTML form checkboxes send the value 'on' or 'off' instead of a boolean
    # value. This is not the case for 'going' because it uses two checkboxes.
    # To convert it to boolean we do some pre-processing before updating
    body["plus_one"] = body.get("plus_one") == 'on'

    try:
        dynamodb.update_rsvp(body)
    except dynamodb.UnknownInviteCodeError:
        # If the code is unknown then show an error page
        return error_page(body["invite_code"])

    # If there was no error then show the success page
    template = jinja2.Environment(
        loader=jinja2.FileSystemLoader('./')
    ).get_template('public/tmpl/success.html')
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "text/html"},
        "body": template.render()
    }
