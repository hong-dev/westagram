from .views import UserView, LoginView

from django.urls import path


urlpatterns = [
        path('/sign-up', UserView.as_view()),
        path('/log-in', LoginView.as_view()),
]
