from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.test_view, name='test'), 
    path('get-claude-response/', views.get_claude_response, name='get-claude-response'),
    path('get-csrf-token/', views.get_csrf_token, name='get-csrf-token'),
]