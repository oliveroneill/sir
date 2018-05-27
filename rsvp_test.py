import dynamodb
import rsvp


def test_rsvp(monkeypatch):
    arguments = []

    def mockreturn(data):
        arguments.append(data)
    monkeypatch.setattr(dynamodb, 'update_rsvp', mockreturn)
    response = rsvp.rsvp({"body": "plus_one=on&invite_code=EF321"}, {})
    assert response["statusCode"] == 200
    assert len(arguments) == 1
    assert arguments[0] == {"plus_one": True, "invite_code": "EF321"}


def test_rsvp_unknown_code(monkeypatch):
    def mockreturn(data):
        raise dynamodb.UnknownInviteCodeError()
    monkeypatch.setattr(dynamodb, 'update_rsvp', mockreturn)
    response = rsvp.rsvp({"body": "plus_one=on&invite_code=EF321"}, {})
    assert response["statusCode"] == 403
