import os

import dynamodb
import jinja2
import rsvp_form
import requests


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

    # Load the template as well to ensure they match
    template = jinja2.Environment(
        loader=jinja2.FileSystemLoader('./')
    ).get_template('public/tmpl/rsvp_form.html')
    # spotify_api_token must specifically be None because missing parameters
    # ome out as empty strings in Jinja2. Luckily None will come out of
    # os.environ.get so this case won't happen in production
    assert response["body"] == template.render(**info, spotify_api_token=None)


def test_rsvp_form_unknown_code(monkeypatch):
    def mockreturn(invite_code):
        raise dynamodb.UnknownInviteCodeError()
    monkeypatch.setattr(dynamodb, 'get_invitee', mockreturn)
    params = {"invite_code": "EF321"}
    response = rsvp_form.rsvp_form({"queryStringParameters": params}, {})
    assert response["statusCode"] == 403


def test_rsvp_form_spotify_token(monkeypatch):
    info = {
        "going": True,
        "food": "vegan",
        "plus_one": False,
        "music": "Sufjan Stevens",
        "notes": "I'll be half an hour late"
    }
    spotify_api_token = "test_token123"

    def mockreturn(invite_code):
        return info
    monkeypatch.setattr(dynamodb, 'get_invitee', mockreturn)

    def mock_spotify_token():
        return spotify_api_token
    monkeypatch.setattr(rsvp_form, 'get_spotify_api_token', mock_spotify_token)

    params = {"invite_code": "EF321"}
    response = rsvp_form.rsvp_form({"queryStringParameters": params}, {})
    assert response["statusCode"] == 200

    # Load the template as well to ensure they match
    template = jinja2.Environment(
        loader=jinja2.FileSystemLoader('./')
    ).get_template('public/tmpl/rsvp_form.html')
    expected = template.render(**info, spotify_api_token=spotify_api_token)
    assert response["body"] == expected


def test_get_spotify_api_token(monkeypatch):
    spotify_api_token = "test_token123"

    def mock_env_return(name):
        return spotify_api_token
    monkeypatch.setattr(os.environ, 'get', mock_env_return)

    def mock_requests(url, data, headers):
        class Response(object):
            def json(self):
                return {"access_token": spotify_api_token}
        return Response()

    monkeypatch.setattr(requests, 'post', mock_requests)

    assert rsvp_form.get_spotify_api_token() == spotify_api_token


def test_get_spotify_api_token_not_set(monkeypatch):
    assert rsvp_form.get_spotify_api_token() is None
