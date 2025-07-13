from django.urls import path
from blog_app import views

urlpatterns = [
    path("",views.post_list, name = "post_list"),
    path('post_details/<int:pk>/', views.view_more, name='post_details'),
    path('post/<int:pk>/', views.post_details, name='post-detail'), 
    path("draft-list/", views.draft_list, name="draft-list"),
    path("post-create/", views.post_create, name="post-create"),
    path("draft-detail/<int:pk>/",views.draft_detail, name="draft-detail"),
    path("post-update/<int:pk>/",views.post_update, name="post-update"),
    path("post-delete/<int:pk>/",views.post_delete,name="post-delete"),
    path("draft-publish/<int:pk>/",views.draft_publish, name = "draft-publish"),
]