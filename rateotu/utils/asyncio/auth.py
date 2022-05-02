from django.db import close_old_connections
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import AnonymousUser

from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.exceptions import (
    AuthenticationFailed,
    InvalidToken,
    TokenError,
)

from rateotu.utils.asyncio.selectors import get_user


class JWTAuthMiddleware:
    """
    JWT authentication middleware for Django Channels 3.
    """

    def __init__(self, app):
        # Store the ASGI application we were passed
        self.app = app

    async def __call__(self, scope, receive, send):
        # Close old database connections to prevent usage of timed out connections
        close_old_connections()

        if "query_string" in scope:
            raw_token = scope["query_string"].decode()
            if raw_token:
                try:
                    validated_token = await self.get_validated_token(raw_token)
                except InvalidToken:
                    scope["user"] = AnonymousUser()
                else:
                    try:
                        scope["user"] = await self.get_user_for_validated_token(
                            validated_token
                        )
                    except (InvalidToken, AuthenticationFailed):
                        scope["user"] = AnonymousUser()
            else:
                scope["user"] = AnonymousUser()
        else:
            scope["user"] = AnonymousUser()

        # Return the inner application directly and let it run everything else
        return await self.app(scope, receive, send)

    async def get_validated_token(self, raw_token):
        """
        Validates an encoded JSON web token and returns a validated token
        wrapper object.
        """
        messages = []
        for AuthToken in api_settings.AUTH_TOKEN_CLASSES:
            try:
                return AuthToken(raw_token)
            except TokenError as e:
                messages.append(
                    {
                        "token_class": AuthToken.__name__,
                        "token_type": AuthToken.token_type,
                        "message": e.args[0],
                    }
                )
        raise InvalidToken(
            {
                "detail": "Given token not valid for any token type",
                "messages": messages,
            }
        )

    async def get_user_for_validated_token(self, validated_token):
        """
        Attempts to find and return a user using the given validated token.
        """
        try:
            validated_id_claim = validated_token[api_settings.USER_ID_CLAIM]
        except KeyError:
            raise InvalidToken("Token contained no recognizable user identification")

        try:
            user = await get_user(api_settings.USER_ID_FIELD, validated_id_claim)
        except ObjectDoesNotExist:
            raise AuthenticationFailed("User not found", code="user_not_found")

        if not user.is_active:
            raise AuthenticationFailed("User is inactive", code="user_inactive")

        return user
