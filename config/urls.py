from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('apps.users_app.urls')),
    path('employees/', include('apps.employees_app.urls')),
    path('accounting/', include('apps.accounting_app.urls')),
    path('calendar/', include('apps.calendar_app.urls')),
]
