from django.contrib.auth.decorators import user_passes_test
from django.urls import path
from django.views.generic.base import TemplateView

from .views import HomeView, VisualizeView
from .views import PostsDetailView
from .views import MyDiscussionsView
from .views import ChooseSchemeView
from .views import CreatePost
from .views import DeletePost
from .views import CounterPost
from argupedia import views

logged_users_redirect = user_passes_test(lambda u: u.is_anonymous, "/")

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path("posts/<int:pk_post>/", PostsDetailView.as_view(), name="posts-detail-view"),
    path("posts/delete/<int:pk_post>/", DeletePost.as_view(), name="posts-delete"),
    path("posts/mydiscussions/<str:username>/", MyDiscussionsView.as_view(), name="my-discussions-view"),
    path("posts/create/choose_scheme/<int:pk_post>/", ChooseSchemeView.as_view(), name="choose-scheme-view"),

    path("posts/create/input_argument/<str:pk_scheme>/", CreatePost.as_view(), name="create-post-view"),
    #path("posts/counter/<str:pk_scheme>/<int:pk_post>/", CounterPost.as_view(), name="counter-post-view"),
    path("posts/counter/<str:pk_scheme>/<int:pk_post>/<int:critical_question_id>/", CounterPost.as_view(), name="counter-post-view"),
    #visualization
    path("posts/visualize/<int:pk_post>/", VisualizeView.as_view(), name="visualize-view"),

    path("posts/upvote/", views.upvote, name="upvote"),
    path("posts/downvote/", views.downvote, name="downvote"),
]