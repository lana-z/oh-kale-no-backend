from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def home_view(request):
    return HttpResponse("oh, kale no!")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('core/', include("core.urls")),
    path('', home_view), 
]