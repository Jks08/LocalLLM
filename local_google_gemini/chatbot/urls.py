from django.urls import path
from .views import *

urlpatterns = [
    # path('', LandingPage.as_view()),
    path('Text', SingleInputDataView.as_view()),
    # path('Chat', ChatInputDataView.as_view())
]