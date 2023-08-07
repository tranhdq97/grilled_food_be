from django.urls import path

from base.common.constant.view_action import BaseViewAction
from staff.address.views.viewset import AddressViewSet

urlpatterns = [
    path("create", AddressViewSet.as_view({"post": BaseViewAction.CREATE})),
    path("list", AddressViewSet.as_view({"get": BaseViewAction.LIST})),
    path("<int:pk>/update", AddressViewSet.as_view({"put": BaseViewAction.UPDATE})),
    path("<int:pk>/delete", AddressViewSet.as_view({"delete": BaseViewAction.DESTROY})),
    path("<int:pk>/detail", AddressViewSet.as_view({"get": BaseViewAction.RETRIEVE})),
]
