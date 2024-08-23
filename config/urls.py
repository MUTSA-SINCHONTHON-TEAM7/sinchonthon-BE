"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from accounts.views import kakao_login, user_my_detail, user_detail
from lectures.views import lecture_post_or_lists, lecture_single, lecture_my, lecture_applied, funding_access
from subjects.views import *
from accounts.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('auth/kakao/login', kakao_login),
    path('users/me', user_my_detail),
    path('users', user_detail),

    path('lectures', lecture_post_or_lists),
    path('lectures/<int:id>', lecture_single),
    path('lectures/my', lecture_my),
    path('lectures/applied', lecture_applied),
    path('fundings', funding_access),

    path('subjects', subject_post),
    path('votes', vote_access),
    path('subjects/complete', get_fundsubjects),
    path('subjects/progress', get_votesubjects),
    path('subjects/<int:id>', get_subject_detail),

    path('search', include('search.urls')),
    path('reviews', include('reviews.urls')),
    
    path('users/credit', insert_credit),
]
