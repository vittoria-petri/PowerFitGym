from django.contrib import admin
from django.urls import path, include

import accounts.views

urlpatterns = [
    path("", accounts.views.HomePageView.as_view(), name="home"),
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")), #new
    path("accounts/", include("django.contrib.auth.urls")), #new
    path("exercises/", include("exercises.urls")),  # new
]
