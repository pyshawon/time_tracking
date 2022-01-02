from rest_framework.permissions import AllowAny
from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .serializers import SignupSerializer


@api_view(['GET'])
def home(request):
    """
    Temporary Home View
    """
    context = {
        "welcome": "Project Time Tracking Application",
        "Swagger": "http://127.0.0.1:8000/swagger/",
        "Redoc": "http://127.0.0.1:8000/redoc/"
    }
    return Response(context)


class SignupUserView(generics.CreateAPIView):
    """
    Create API View Signup User.
    """
    model = User
    permission_classes = [AllowAny]
    serializer_class = SignupSerializer


class LoginUserView(ObtainAuthToken):
    """
    obtain_auth_token using as a login view.
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'username': user.username,
        })
