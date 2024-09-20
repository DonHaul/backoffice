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
    
    from django.http import HttpResponseRedirect
    def pre_social_login(self, request, sociallogin):
        print("PRE SOCIAL SIGNUP")
        print(str(request.user))
        print(str(sociallogin.user))


        # Extract email from the social login data
        email = sociallogin.account.extra_data.get('email')
        
        # If email is missing, redirect to the 'fill-email' page
        if not email:
            request.session['sociallogin'] = sociallogin.serialize()  # Store social login data in session
            return HttpResponseRedirect(reverse('fill_email')) 

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
