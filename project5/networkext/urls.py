from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("post", views.post, name="post_view"),
    path("like_post", views.like_post, name="like_post"),
    path("friend_request", views.friend_request, name="friend_request"),
    path("profile/<int:user_id>", views.profile, name="profile"),
    path("message", views.message, name="message"),
    path("react_post", views.react_post, name="react_post"),
    path("react_message", views.react_message, name="react_message"),
    path("react_message_send/<int:user_id>", views.react_message_send, name="react_message_send"),
    path("react_messages", views.messages, name="messages"),
]