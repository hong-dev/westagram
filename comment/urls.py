from .views import CommentView

from django.urls import path

urlpatterns = [
        path('', CommentView.as_view()),
]
