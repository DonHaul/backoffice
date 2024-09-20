from __future__ import annotations

import typing

from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings
from django.http import HttpRequest

if typing.TYPE_CHECKING:
    from allauth.socialaccount.models import SocialLogin

    from backoffice.users.models import User


class AccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request: HttpRequest) -> bool:
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_open_for_signup(
        self, request: HttpRequest, sociallogin: SocialLogin
    ) -> bool:
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)
    
    import urllib.parse
    from django.http import HttpResponseRedirect
    def pre_social_login(self, request, sociallogin):
        print("PRE SOCIAL SIGNUP")
        print(str(request.user))
        print(str(request))
        print(request.META)
        print(sociallogin.serialize())

    #     import urllib
    #     email = sociallogin.account.extra_data.get('email')
    # # If email is missing, serialize the social login data and pass it to Flask
    #     if not email:
    #         # Serialize the social login data
    #         sociallogin_data = sociallogin.serialize()
    #         session_token = request.session.session_key  # Optional: Store session key for further authentication

    #         # URL encode the social login data to send it securely to Flask
    #         flask_redirect_url = 'http://localhost:5000/fill-email'
    #         query_params = {
    #             'sociallogin': urllib.parse.quote(sociallogin_data),
    #             'session_token': session_token
    #         }

    #         url_with_params = f"{flask_redirect_url}?{urllib.parse.urlencode(query_params)}"
    #         return HttpResponseRedirect(url_with_params)


    def populate_user(
        self,
        request: HttpRequest,
        sociallogin: SocialLogin,
        data: dict[str, typing.Any],
    ) -> User:
        """
        Populates user information from social provider info.

        See: https://django-allauth.readthedocs.io/en/latest/advanced.html?#creating-and-populating-user-instances
        """
        print("adapter is adapting")
        user = sociallogin.user
        if name := data.get("name"):
            user.name = name
        elif first_name := data.get("first_name"):
            user.name = first_name
            if last_name := data.get("last_name"):
                user.name += f" {last_name}"
        return super().populate_user(request, sociallogin, data)
