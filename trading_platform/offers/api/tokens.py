from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.utils import jwt_decode_handler


def make_token(object):
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    payload = jwt_payload_handler(object)
    token = jwt_encode_handler(payload)
    return token


def decode_token(token):
    decoded_payload = jwt_decode_handler(token)
    return decoded_payload
