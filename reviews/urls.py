from django.urls import path
from .views import review, review_delete

urlpatterns = [
    path('', review),
    path('/<int:id>', review_delete),
]