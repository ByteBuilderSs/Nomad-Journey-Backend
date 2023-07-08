from django.urls import path
from .views import *


urlpatterns = [
    path('posts/' , PublicBlogView.as_view()),
    path('general-posts/' , GeneralBlogView),
    path('userpost/' , BlogView.as_view()),
    path('post/<str:slug>' , BlogDetailView.as_view()),
    path('tags/' , TagView.as_view()),
    path('tagdetail/<uid>' , TagViewByUid.as_view()),
    path('others-profile-post/<str:username>' , BlogViewUserForView.as_view()),
    path('search-blog/', SearchBlog.as_view()),
    path('most-liked-blog/', MostLikedBlogView.as_view()),
    path('author-liked-blog/<str:username>', AuthorLikedBlog.as_view())
]