"""ec_staff URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, include

handler500 = "base.common.custom.exceptions.server_error"

urlpatterns = [
    path("", include("base.urls")),
    path("api/address/", include("staff.address.urls"), name="address"),
    path("api/profile/", include("staff.profile.urls"), name="profile"),
    path("api/staff/", include("staff.staff.urls"), name="staff"),
    path("api/item/", include("staff.item.urls"), name="item"),
    path("api/table/", include("staff.table.urls"), name="table"),
    path("api/order/", include("staff.order.urls"), name="order"),
]
