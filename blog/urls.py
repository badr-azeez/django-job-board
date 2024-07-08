from django.urls import path
from . import views
app_name = 'blog'

urlpatterns = [
    path('',views.PostList.as_view(),name="blog_posts"),
    path('comment/<slug:slug>/',views.CommentDetail.as_view(),name="comment"),
    path('comment/<slug:slug>/delete',views.CommentDelete.as_view(),name="delete_comment"),
    path('<slug:slug>',views.PostDetail.as_view(),name="post_details")
]
