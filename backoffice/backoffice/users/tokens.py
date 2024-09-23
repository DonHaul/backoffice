
from django.http import HttpRequest
from urllib.parse import urljoin
from django.urls import reverse
import requests
from allauth.headless.tokens.sessions import SessionTokenStrategy

class BasicTokenStrategy(SessionTokenStrategy):
    def create_access_token(self, request):
        return f"at-user-{request.user.pk}"
