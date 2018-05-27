import dynamodb
import jinja2
import rsvp_form


def test_rsvp_form(monkeypatch):
    info = {
        "going": True,
        "food": "vegan",
        "plus_one": False,
        "music": "Sufjan Stevens",
        "notes": "I'll be half an hour late"
    }

    def mockreturn(invite_code):
        return info
    monkeypatch.setattr(dynamodb, 'get_invitee', mockreturn)
    params = {"invite_code": "EF321"}
    response = rsvp_form.rsvp_form({"queryStringParameters": params}, {})
    assert response["statusCode"] == 200

    template = jinja2.Environment(
        loader=jinja2.FileSystemLoader('./')
    ).get_template('rsvp_form.html')
    assert response["body"] == template.render(**info)


def test_rsvp_form_unknown_code(monkeypatch):
    def mockreturn(invite_code):
        raise dynamodb.UnknownInviteCodeError()
    monkeypatch.setattr(dynamodb, 'get_invitee', mockreturn)
    params = {"invite_code": "EF321"}
    response = rsvp_form.rsvp_form({"queryStringParameters": params}, {})
    assert response["statusCode"] == 403
