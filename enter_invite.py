"""
A handler for displaying the invite code page.

This is the initial page that the user will see.

This handler doesn't currently require any templating but it
was easier to use this, as it's already used for other handlers.
It also offers the option to start templating here when needed.
"""
import jinja2


def invite_form(event, context):
    """Get response for invite code page. Invoked by AWS Lambda."""
    template = jinja2.Environment(
        loader=jinja2.FileSystemLoader('./')
    ).get_template('enter_invite.html')
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "text/html"},
        "body": template.render()
    }
