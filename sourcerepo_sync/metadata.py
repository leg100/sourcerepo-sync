import requests


def service_account():
    return _request('email').text


def access_token():
    return _token()['access_token']


def _token():
    return _request('token').json()


def _request(detail):
    url = ('http://metadata.google.internal',
        f'/computeMetadata/v1/instance/service-accounts/default/{detail}')

    return requests.get(url, headers={'Metadata-Flavor': 'Google'})
