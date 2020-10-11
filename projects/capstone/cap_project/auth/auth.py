import json
from flask import request, _request_ctx_stack, abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen


# https://onlineeducation.eu.auth0.com/authorize?audience=CourseAndDomain&response_type=token&client_id=tEepmn5J6Lm2jIjNDQ2Mm15GNh9sG5x0&redirect_uri=http://0.0.0.0:8080

AUTH0_DOMAIN = 'onlineeducation.eu.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'CourseAndDomain'

## AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

## Auth Header
'''
    atempts to get the header from the request
    raises an AuthError if no header is present
    attempts to split bearer and the token
    raises an AuthError if the header is malformed
    returns the token part of the header
'''
def get_token_auth_header():
    if 'Authorization' not in request.headers:
        raise AuthError('No authorization header', 401)
    
    auth_header = request.headers['Authorization']
    header_parts = auth_header.split(' ')

    if len(header_parts) != 2:
        raise AuthError('Please use bearer authorization token', 401)
    elif header_parts[0].lower() != 'bearer':
        raise AuthError('Please use bearer authorization token', 401)
    return header_parts[1]

'''
    @INPUTS
        permission: string permission (i.e. 'post:domain')
        payload: decoded jwt payload

    it should raise an AuthError if permissions are not included in the payload
    it should raise an AuthError if the requested permission string is not in the payload permissions array
    return true otherwise
'''
def check_permissions(permission, payload):
    if permission not in payload['permissions']:
        raise AuthError('You do not have the permission to perform that action', 401)
    return True

'''
verify_decode_jwt(token) method
    @INPUTS
        token: a json web token (string)
    it should be an Auth0 token with key id (kid)
    it should verify the token using Auth0 /.well-known/jwks.json
    it should decode the payload from the token
    it should validate the claims
    return the decoded payload

    !!NOTE urlopen has a common certificate error described here: https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org
'''
def verify_decode_jwt(token):
    # Using the boilerplate from the lesson

    # get the public key from auth0
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    
    # get the data in the header
    unverified_header = jwt.get_unverified_header(token)

    # choose key
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
    }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            # USE THE KEY TO VALIDATE THE JWT
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
            }, 400)

'''
@requires_auth(permission) decorator method
    @INPUTS
        permission: string permission (i.e. 'post:domains')

    it should use the get_token_auth_header method to get the token
    it should use the verify_decode_jwt method to decode the jwt
    it should use the check_permissions method validate claims and check the requested permission
    return the decorator which passes the decoded payload to the decorated method
'''
def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)
        return wrapper
    return requires_auth_decorator
