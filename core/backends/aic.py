"""
Akamai Identity Cloud (AIC) - compatible with Hosted Login v2
"""
from jose import jwt
from urllib.parse import urljoin
from .oauth import BaseOAuth2


class AicOAuth2(BaseOAuth2):
    """AIC Hosted Login v2 authentication backend"""
    name = 'aic'
    SCOPE_SEPARATOR = ' '
    DEFAULT_SCOPE = ['openid profile email']
    REDIRECT_STATE = False
    ACCESS_TOKEN_METHOD = 'POST'
    EXTRA_DATA = [
        ('picture', 'picture'),
        ('iss', 'iss')
    ]

    def api_path(self, path=''):
        """Build API path for AIC domain"""
        return 'https://{domain}/{path}'.format(domain=self.setting('DOMAIN'), path=path)

    def authorization_url(self):
        return self.api_path('login/authorize')

    def access_token_url(self):
        return self.api_path('login/token')

    def get_user_id(self, details, response):
        """Return current user id."""
        return details['user_id']

    def get_user_details(self, response):
        # Obtain JWT and the keys to validate the signature
        id_token = response.get('id_token')
        jwks = self.get_json(self.api_path('login/jwk'))
        issuer = self.api_path('login')
        audience = self.setting('KEY')
        payload = jwt.decode(id_token,
                             jwks,
                             algorithms=['RS256'],
                             audience=audience,
                             issuer=issuer,
                             access_token=response.get('access_token'))

        # As specified in social_core/backends/base.py
        return {
             'user_id':id_token,
             'picture': None,
             'username': payload['preferred_username'],
             #'email': payload['email'],
             'fullname': payload['preferred_username'],
             'first_name': payload['preferred_username'],
             'last_name': payload.get('family_name', False) }

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        return self._user_data(access_token)

    def _user_data(self, access_token, path=None):
        """Convenience method for userinfo data"""
        url = self.api_path('/profiles/oidc/userinfo')
        return self.get_json(url, headers={'Authorization': 'Bearer {0}'.format(access_token)})

