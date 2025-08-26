from django.urls import path
from .views import PostListAPI,PostDetailAPI,PostListCreateAPI,PostUpdateAPI,PostDeleteAPI,DraftListAPI,DraftDetailAPI,DraftPublishAPI
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("posts/",PostListAPI.as_view(),name="api-post-list"),
    path("post_details/<int:pk>/",PostDetailAPI.as_view(),name = "api-post-detail"),
    path("post_create/",PostListCreateAPI.as_view(),name="api-post-create"),
    path("post_update/<int:pk>/",PostUpdateAPI.as_view(),name="api-post-update"),
    path("post_delete/<int:pk>/",PostDeleteAPI.as_view(),name="api-post-delete"),
    path("draft_list/",DraftListAPI.as_view(),name="api-draft-list"),
    path("draft_detail/<int:pk>/",DraftDetailAPI.as_view(),name="api-deaft-detail"),
    path("draft_publish/<int:pk>/", DraftPublishAPI.as_view(), name="draft-publish"),
    path("token/",TokenObtainPairView.as_view(),name="token_obtain_pair"),
    path("token/refresh/",TokenRefreshView.as_view(),name="token_refresh")
]