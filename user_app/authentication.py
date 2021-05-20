from .models import Token
from django.utils.six import text_type
from rest_framework import HTTP_HEADER_ENCODING, exceptions

def get_authorization_header(request):
    """
    Return request's 'Authorization:' header, as a bytestring.

    Hide some test client ickyness where the header can be unicode.
    """
    auth = request.META.get('HTTP_AUTHORIZATION', b'')
    if isinstance(auth, text_type):
        # Work around django test client oddness
        auth = auth.encode(HTTP_HEADER_ENCODING)
    return auth


class MyTokenAuthentication(object):
    """
    Simple token based authentication.

    Clients should authenticate by passing the token key in the "Authorization"
    HTTP header, prepended with the string "Token ".  For example:

        Authorization: Token 401f7ac837da42b97f613d789819ff93537bee6a
    """

    keyword = 'Token'
    model = None

    def get_model(self):
        if self.model is not None:
            return self.model
        return Token

    """
    A custom token model may be used, but must have the following properties.

    * key -- The string identifying the token
    * user -- The user to which the token belongs
    """

    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None

        if len(auth) == 1:
            # msg = 'Invalid token header. No credentials provided.'
            msg = "Неверный заголовок с токеном. Данные не предоставлены"
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            # msg = 'Invalid token header. Token string should not contain spaces.'
            msg = "Неверный заголовок с токеном. Токен не должен содержать пробелов"
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = auth[1].decode()
        except UnicodeError:
            # msg = 'Invalid token header. Token string should not contain invalid characters.'
            msg = "Неверный заголовок с токеном. Токен не должен содержать лишних символов"
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(token)

    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = model.objects.select_related('user').get(key=key, is_active=True)
        except model.DoesNotExist:
            # msg = 'Invalid token.'
            msg = "Неверный токен"
            raise exceptions.AuthenticationFailed(msg)

        if not token.user.is_active:
            # mgs = 'User inactive or deleted.'
            msg = "Пользователь не активен или удален"
            raise exceptions.AuthenticationFailed(msg)

        return (token.user, token)

    def authenticate_header(self, request):
        return self.keyword