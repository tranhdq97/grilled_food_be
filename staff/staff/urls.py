from django.urls import path

from base.common.constant.view_action import BaseViewAction
from staff.staff.views.viewset import StaffViewSet

urlpatterns = [
    path("create", StaffViewSet.as_view({"post": BaseViewAction.CREATE})),
    path("list", StaffViewSet.as_view({"get": BaseViewAction.LIST})),
    path("<int:pk>/update", StaffViewSet.as_view({"put": BaseViewAction.UPDATE})),
    path("<int:pk>/detail", StaffViewSet.as_view({"get": BaseViewAction.RETRIEVE})),
    path("<int:pk>/delete", StaffViewSet.as_view({"delete": BaseViewAction.DESTROY})),
]
