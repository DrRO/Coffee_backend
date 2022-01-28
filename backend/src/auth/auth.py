import json
from flask import request, _request_ctx_stack
from functools import wraps
from flask import request, abort
from jose import jwt
from urllib.request import urlopen

AUTH0_DOMAIN = 'mycoffeeshop-project.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'coffee'

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

# Done implement get_token_auth_header() method
def get_token_auth_header():
    # raise an AuthError if no header is present
    if "Authorization" not in request.headers:
        raise AuthError({
            "code": "invalid_header",
            "description": "header is missing"
        }, 401)

    header = request.headers["Authorization"].split()
    bearer_prefix = header[0]
    token = header[1]

    # raise an AuthError if the header is malformed
    if len(header) > 2:
        raise AuthError({
            "code": "invalid_header",
            "description": "header is malformed"
        }, 401)

    #  handling 401 error
    if not bearer_prefix:
        raise AuthError({
            "code": "invalid_header",
            "description": "header is missing bearer prefix"
        }, 401)

    return token


# Done implement check_permissions(permission, payload) method

def check_permissions(permission, payload):
    if 'permissions' not in payload:
                        raise AuthError({
                            'code': 'invalid_claims',
                            'description': 'Permissions not included in JWT.'
                        }, 400)

    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Permission not found.'
        }, 403)
    return True

# implement verify_decode_jwt(token) method


def verify_decode_jwt(token: str):
    # Get data from Auth0
    jsonurl = urlopen(f"https://{AUTH0_DOMAIN}/.well-known/jwks.json")
    jwks = json.loads(jsonurl.read())


    rsa_key = {}
    # check the data in the header
    if "kid" not in jwt.get_unverified_header(token):
        raise AuthError({
            "code": "INVALID_HEADER",
            "description": "Authorization header is malformed"
        }, 401)

    for key in jwks["keys"]:
        if key["kid"] == jwt.get_unverified_header(token)["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"]
            }
    # Token validation by the rsa_key
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer=f"https://{AUTH0_DOMAIN}/"
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                "code": "TOKEN_EXPIRED",
                "description": "Token expired"
            }, 401)
        except Exception:
            raise AuthError({
                "code": "INVALID_HEADER",
                "description": "Unable to parse authentication token"
            },"400_BAD_REQUEST")

        except jwt.JWTClaimsError:
            raise AuthError({
                "code": "INVALID_CLAIMS",
                "description": "Incorrect claims. Please, check the audience and issuer"
            }, "401_UNAUTHORIZED")



    raise AuthError({
        "code": "INVALID_HEADER",
        "description": "Unable to find the appropriate key"
    }, 400)





# implement @requires_auth(permission) decorator method
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




