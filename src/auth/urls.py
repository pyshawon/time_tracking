from django.urls import path
from .views import SignupUserView, LoginUserView


urlpatterns = [
    path('signup/', SignupUserView.as_view(), name='sign-up'),
    path('login/', LoginUserView.as_view(), name='login'),
]
