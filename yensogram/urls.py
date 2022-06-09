from django.urls import path

from . import views



urlpatterns = [
    path("", views.index, name="yg-index"),
    path("register/", views.register, name="yg-register"),
    path("login/", views.login_view, name="yg-login"),
    path("logout/", views.logout_view, name="yg-logout"),
    path("account/<str:username>/", views.account, name="yg-account"),
    path("add/", views.add, name="yg-add"),
    path("friend-requests/", views.friend_requests, name="yg-friend-requests"),
    path("friend-request-accept/<str:username>", views.friend_request_accept, name="yg-friend-request-accept"),
    path("friend-request-decline/<str:username>", views.friend_request_decline, name="yg-friend-request-decline"),
    path("messages/<str:friend>", views.messages, name="yg-messages"),
    path("post/new", views.new_post, name="yg-new-post"),
    path("post/<int:post_id>", views.post, name="yg-post"),
    
    # API Routes
    path("messages_API/<str:friend>", views.messages_API),
    path("messages_count_API/<str:username>", views.unopened),
    
]

