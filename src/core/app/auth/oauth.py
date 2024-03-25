from flask_oauthlib.provider import OAuth2Provider
from src.core.app.app import app
from src.core.app.models.models import db, OAuthClient, OAuthToken

oauth = OAuth2Provider(app)

@oauth.clientgetter
def load_client(client_id):
    """
    Retrieve an OAuthClient instance by its client_id.

    This function is used by the OAuth2Provider to fetch the client details
    necessary for the OAuth flow.
    """
    return OAuthClient.query.filter_by(client_id=client_id).first()

@oauth.tokengetter
def load_token(access_token=None, refresh_token=None):
    """
    Retrieve an OAuthToken instance using either an access token or a refresh token.

    This function is utilized by the OAuth2Provider to obtain the token details
    for validating OAuth requests.
    """
    if access_token:
        return OAuthToken.query.filter_by(access_token=access_token).first()
    elif refresh_token:
        return OAuthToken.query.filter_by(refresh_token=refresh_token).first()

@oauth.tokensetter
def save_token(token, request, *args, **kwargs):
    """
    Save a new token and remove old tokens for the same client and user.
    """
    tokens = OAuthToken.query.filter_by(client_id=request.client.client_id, user_id=request.user.id).all()
    # Логіка для збереження нового токену, видалення старих токенів
