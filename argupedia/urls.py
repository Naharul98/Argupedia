from django.contrib.auth.decorators import user_passes_test
from django.urls import path
from django.views.generic.base import TemplateView

from .views import HomeView
from .views import PostsDetailView
from .views import MyDiscussionsView


logged_users_redirect = user_passes_test(lambda u: u.is_anonymous, "/")

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path("posts/<int:pk_post>/", PostsDetailView.as_view(), name="posts-detail-view"),

    path("posts/mydiscussions/<str:username>/", MyDiscussionsView.as_view(), name="my-discussions-view"),


]