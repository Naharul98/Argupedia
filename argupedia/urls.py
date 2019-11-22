from django.contrib.auth.decorators import user_passes_test
from django.urls import path
from django.views.generic.base import TemplateView

from .views import HomeView

logged_users_redirect = user_passes_test(lambda u: u.is_anonymous, "/")

urlpatterns = [
    path('', HomeView.as_view(), name='home'),

]