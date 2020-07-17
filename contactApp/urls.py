from django.urls import path

from contactApp import views

urlpatterns = [
    path('syncContacts/', views.sync_user_contacts),
    path('registerUser/', views.register_user)
]
