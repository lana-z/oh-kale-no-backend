from django.urls import path
from . import views

urlpatterns = [
    path('get-claude-response/', views.get_claude_response, name='get-claude-response'),
    path('get-csrf-token/', views.get_csrf_token, name='get-csrf-token'),
    path('visit-count/', views.get_visit_count, name='visit-count'),
    path('increment-visit/', views.increment_visit_count, name='increment-visit'),
]