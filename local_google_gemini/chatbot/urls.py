from django.urls import path
from .views import *
from .views_frontend import *

urlpatterns = [
    path('', LandingPage.as_view()),
    # path('', index),
    path('Text', SingleInputDataView.as_view()),
    path('ChatFrontEnd', chat_page),
    path('ClearHistory', ClearHistory),
]