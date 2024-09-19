import requests
from urllib.parse import urljoin
from django.urls import reverse

from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.providers.orcid.views import OrcidOAuth2Adapter
from dj_rest_auth.registration.views import SocialConnectView, SocialLoginView
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.views import APIView
from backoffice.users.api.serializers import UserSerializer

User = get_user_model()


class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "pk"

    def get_queryset(self, *args, **kwargs):
        assert isinstance(self.request.user.id, int)
        return self.queryset.filter(id=self.request.user.id)

    @action(detail=False)
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)


from django.conf import settings
class OrcidLogin(SocialLoginView):
    adapter_class = OrcidOAuth2Adapter
    client_class = OAuth2Client
    callback_url = "http://localhost:8000/api/v1/auth/google/callback/"


class OrcidConnect(SocialConnectView):
    adapter_class = OrcidOAuth2Adapter


class OrcidLoginCallback(APIView):
    def get(self, request, *args, **kwargs):
        """
        If you are building a fullstack application (eq. with React app next to Django)
        you can place this endpoint in your frontend application to receive
        the JWT tokens there - and store them in the state
        """

        code = request.GET.get("code")

        if code is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        # Remember to replace the localhost:8000 with the actual domain name before deployment
        token_endpoint_url = urljoin("http://localhost:8000", reverse("orcid_login"))
        response = requests.post(url=token_endpoint_url, data={"code": code})

        return Response(response.json(), status=status.HTTP_200_OK)
