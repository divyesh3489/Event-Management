from django.urls import path, include

urlpatterns = [
    path('', include('events.urls')),
    path('users/', include('users.urls')),
]
