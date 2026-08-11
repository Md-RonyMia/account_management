from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('analytics/', include('analytics.urls')),
    path('inventory/', include('inventory.urls')),
    path('purchasing/', include('purchasing.urls')),
]